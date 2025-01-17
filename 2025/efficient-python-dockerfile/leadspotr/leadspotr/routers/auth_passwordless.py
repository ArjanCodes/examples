from typing import Annotated

from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ..config import settings
from ..db import database
from ..db.crud.company import create_company
from ..db.crud.user import create_user, get_user_by_email
from ..db.models import RoleEnum
from ..db.schemas.company import CompanyCreate
from ..db.schemas.user import User, UserCreate, UserRegister
from ..dependencies.authentication import get_current_user
from ..email import email_client
from ..utils.security import (
    create_access_token,
    create_invite_token,
    decode_invite_token,
    set_auth_cookie,
)
from .router import APIRouter

router = APIRouter()

router.prefix = "/auth/passwordless"


@router.post("/signup")
def register_user(
    current_user: Annotated[User | None, Depends(get_current_user)],
    registration_data: UserRegister,
    db: Session = Depends(database.get_db),
) -> dict:
    if current_user is not None:
        raise HTTPException(status_code=400, detail="Already logged in")

    db_user = get_user_by_email(db, email=registration_data.email)
    if db_user is not None:
        raise HTTPException(status_code=409, detail="Email already registered")
    db_company = create_company(
        db=db,
        company=CompanyCreate(name=registration_data.company_name),
    )

    user_registration_data = UserCreate(
        email=registration_data.email,
        name=registration_data.name,
        company_id=db_company.id,
        role=RoleEnum.admin,
    )

    db_user = create_user(db=db, user=user_registration_data)
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
            recipients=[registration_data.email],
            subject=f"Thanks for logging in, {db_user.name}!",
            data=data,
            template_id=settings.SENDGRID_SIGNUP_TEMPLATE_ID,
        )
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return {"status": 200, "message": "User created"}


@router.post("/request-login")
def request_passwordless_login(
    current_user: Annotated[User | None, Depends(get_current_user)],
    email: str,
    db: Session = Depends(database.get_db),
) -> dict:
    if current_user is not None:
        raise HTTPException(status_code=400, detail="Already logged in")

    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    token_info = {
        "id": user.id,
    }

    token = create_invite_token(token_info)

    data = {
        "name": user.name,
        "verificationUrl": f"{settings.FRONTEND_URL}/auth/verify-login/{token}",
    }

    try:
        email_client.send_mail(
            recipients=[email],
            subject=f"Thanks for logging in, {user.name}!",
            data=data,
            template_id=settings.SENDGRID_LOGIN_TEMPLATE_ID,
        )
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return {"message": "Email successfully sent"}


@router.get("/verify-login")
def verify_passwordless_login(
    token: str,
    response: Response,
    current_user: Annotated[User | None, Depends(get_current_user)],
) -> dict:
    if current_user is not None:
        raise HTTPException(status_code=400, detail="Already logged in")

    token_info = decode_invite_token(token)

    if token_info is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    token = create_access_token(token_info)

    set_auth_cookie(response=response, token=token)

    return {"status": 200, "message": f"User {token_info['id']} successfully logged in"}
