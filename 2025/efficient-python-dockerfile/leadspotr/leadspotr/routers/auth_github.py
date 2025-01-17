from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..config import settings
from ..db import database
from ..db.crud.company import create_company
from ..db.crud.user import create_user, get_user_by_email
from ..db.models import RoleEnum
from ..db.schemas.company import CompanyCreate
from ..db.schemas.user import User, UserCreate
from ..dependencies.authentication import (
    get_current_user,
    get_github_access_token,
    get_github_user,
)
from ..utils.security import create_access_token, set_auth_cookie
from .router import APIRouter

router = APIRouter()

router.prefix = "/auth/github"


@router.get("/request-login")
def request_github_login(
    current_user: Annotated[User | None, Depends(get_current_user)],
):
    if current_user is not None:
        raise HTTPException(status_code=400, detail="Already logged in")

    return {
        "url": f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}",
        "status": 200,
    }


@router.get("/verify-login")
def verify_github_login(
    current_user: Annotated[User | None, Depends(get_current_user)],
    code: str,
    db: Session = Depends(database.get_db),
) -> RedirectResponse:
    if current_user is not None:
        raise HTTPException(status_code=400, detail="Already logged in")

    github_access_token = get_github_access_token(code)

    github_user = get_github_user(access_token=github_access_token)

    if github_user["email"] is None:
        raise HTTPException(
            status_code=400,
            detail="Your GitHub account must have a public email address to log in",
        )

    db_user = get_user_by_email(db, email=github_user["email"])

    if db_user is None:
        db_company = create_company(
            db=db,
            company=CompanyCreate(name=github_user["login"]),
        )

        user_name = github_user["name"] or github_user["login"]

        user_registration_data = UserCreate(
            email=github_user["email"],
            name=user_name,
            company_id=db_company.id,
            role=RoleEnum.admin,
        )

        db_user = create_user(db=db, user=user_registration_data)

    token_info = {
        "id": db_user.id,
    }

    token = create_access_token(token_info)

    redirect_response = RedirectResponse(url=settings.FRONTEND_URL, status_code=302)

    set_auth_cookie(response=redirect_response, token=token)

    return redirect_response
