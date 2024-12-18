from typing import Annotated, Any

from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ..db import database
from ..db.crud.company import create_company
from ..db.crud.user import create_user, get_user_by_email
from ..db.models import RoleEnum
from ..db.schemas.company import CompanyCreate
from ..db.schemas.user import User, UserCreate, UserLogin, UserRegister
from ..dependencies.authentication import get_current_user
from ..utils.security import (
    create_access_token,
    get_password_hash,
    set_auth_cookie,
    verify_password,
)
from .router import APIRouter

router = APIRouter()

router.prefix = "/auth/with-email-password"


@router.post("/signup")
def register_user(
    response: Response,
    current_user: Annotated[User | None, Depends(get_current_user)],
    registration_data: UserRegister,
    db: Session = Depends(database.get_db),
) -> dict[str, Any]:
    if current_user is not None:
        raise HTTPException(status_code=400, detail="Already logged in")

    db_user = get_user_by_email(db, email=registration_data.email)
    if db_user is not None:
        raise HTTPException(status_code=409, detail="Email already registered")
    db_company = create_company(
        db=db,
        company=CompanyCreate(name=registration_data.company_name),
    )

    if registration_data.password is None:
        raise HTTPException(status_code=400, detail="Password not provided")

    hashed_password = get_password_hash(registration_data.password)

    user_registration_data = UserCreate(
        email=registration_data.email,
        name=registration_data.name,
        company_id=db_company.id,
        role=RoleEnum.admin,
        hashed_password=hashed_password,
    )

    db_user = create_user(db=db, user=user_registration_data)
    token_info = {
        "id": db_user.id,
    }

    token = create_access_token(token_info)

    set_auth_cookie(response=response, token=token)

    return {"status": 200, "message": "User created"}


@router.post("/request-login")
def request_login(
    response: Response,
    current_user: Annotated[User | None, Depends(get_current_user)],
    login_data: UserLogin,
    db: Session = Depends(database.get_db),
) -> dict[str, Any]:
    if current_user is not None:
        raise HTTPException(status_code=400, detail="Already logged in")

    user = get_user_by_email(db, email=login_data.email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(
        plain_password=login_data.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token_info = {
        "id": user.id,
    }

    token = create_access_token(token_info)

    set_auth_cookie(response=response, token=token)

    return {"message": "Successfully logged in", "status": 200}
