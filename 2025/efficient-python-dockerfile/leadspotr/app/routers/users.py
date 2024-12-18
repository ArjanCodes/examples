from typing import Any
from uuid import UUID

from fastapi import Body, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ..config import settings
from ..db import database
from ..db.crud.company import get_company_by_user_id
from ..db.crud.user import get_user_by_email, get_user_by_id, update_user
from ..db.schemas.user import User, UserUpdate
from ..dependencies.authentication import get_current_user
from ..email import email_client
from ..utils.security import create_invite_token, delete_auth_cookie
from .router import APIRouter

router = APIRouter()


@router.get("/users/{id}", response_model=User)
def get(
    id: UUID,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.id != id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db_user = get_user_by_id(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/{id}", response_model=User)
def update(
    id: UUID,
    user_update_data: UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: User | None = Depends(get_current_user),
) -> User:
    if current_user is None:
        raise HTTPException(status_code=400, detail="Not logged in")

    if current_user.id != id:
        raise HTTPException(status_code=403, detail="Forbidden")

    db_user = get_user_by_id(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_user(db, id, user=user_update_data)
    return db_user


@router.get("/me", response_model=User | None)
def get_me(
    current_user: User | None = Depends(get_current_user),
) -> User | None:
    if current_user is None:
        return None

    return current_user


@router.post("/users/logout")
def logout(
    response: Response,
    current_user: User | None = Depends(get_current_user),
) -> dict[str, Any]:
    if current_user is None:
        raise HTTPException(status_code=400, detail="Not logged in")
    # Delete token
    delete_auth_cookie(response=response)

    return {"status": 200, "message": "User logged out"}


# Accept invite
@router.post(
    "/users/accept-invite",
)
def accept_invite(
    inviteCode: str = Body(...),
    email: str = Body(...),
    name: str = Body(...),
    db: Session = Depends(database.get_db),
):
    db_user = get_user_by_email(db, email=email)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.active:
        raise HTTPException(status_code=400, detail="User already active")

    db_company = get_company_by_user_id(db, user_id=db_user.id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    if db_company.invite_code != inviteCode:
        raise HTTPException(status_code=400, detail="Invalid invite code")

    update_data = {"name": name, "active": True}

    db_user = update_user(db, id=db_user.id, user=UserUpdate(**update_data))

    token_info = {
        "id": db_user.id,
    }

    token = create_invite_token(token_info)

    data = {
        "name": db_user.name,
        "verificationUrl": f"{settings.FRONTEND_URL}/auth/verify-login/{token}",
    }

    try:
        email_client.send_mail(
            recipients=[email],
            subject=f"Thanks for logging in, {db_user.name}!",
            data=data,
            template_id=settings.SENDGRID_LOGIN_TEMPLATE_ID,
        )
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return {"message": "User accepted invite", "status": 200}
