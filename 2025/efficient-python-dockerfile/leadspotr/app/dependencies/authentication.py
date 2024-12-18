from typing import Any
from uuid import UUID

import requests
from fastapi import Depends, Request
from sqlalchemy.orm import Session

from ..config import settings
from ..db import database
from ..db.crud.user import get_user_by_id
from ..db.schemas.user import User
from ..utils.security import decode_access_token

# Github OAuth


def get_github_access_token(code: str) -> str:
    """This function retrieves the access token from Github"""
    response = requests.post(
        url="https://github.com/login/oauth/access_token",
        data={
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
        },
        headers={"Accept": "application/json"},
        timeout=10,
    )

    response_json = response.json()
    access_token = response_json["access_token"]

    return access_token


def get_github_user(access_token: str) -> dict[str, Any]:
    """This function retrieves the user data from Github"""
    response = requests.get(
        url="https://api.github.com/user",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        timeout=10,
    )

    github_user = response.json()

    return github_user


async def get_auth_token(request: Request) -> str | None:
    """This dependency retrieves the auth token from the request"""
    auth_token = request.cookies.get(settings.AUTH_TOKEN_COOKIE_NAME)
    return auth_token or None


async def get_current_user(
    _request: Request,
    auth_token: str | None = Depends(get_auth_token),
    db: Session = Depends(database.get_db),
) -> User | None:
    """This is a dependency to check the current user and make the route protected"""
    if not auth_token:
        return None
    payload = decode_access_token(auth_token)

    if payload is None:
        return None

    id: UUID | None = payload.get("id")

    if id is None:
        return None

    user = get_user_by_id(db=db, id=id)

    if not user:
        return None
    return user
