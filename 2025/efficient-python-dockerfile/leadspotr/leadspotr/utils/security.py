import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Response
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext

from ..config import Environment, settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_jwt(
    data: dict[str, Any],
    algorithm: str,
    secret_key: str,
    expires_delta: timedelta,
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta

    payload = {
        key: str(value) for key, value in data.items() if isinstance(value, uuid.UUID)
    }

    payload.update({"exp": expire})

    return jwt.encode(payload, secret_key, algorithm)


def decode_jwt(
    token: str,
    algorithm: str = settings.ALGORITHM,
    secret_key: str = settings.ACCESS_TOKEN_SECRET_KEY,
) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        return None


def create_access_token(
    data: dict[str, Any],
) -> str:
    return generate_jwt(
        data=data,
        algorithm=settings.ALGORITHM,
        secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_DAYS),
    )


def decode_access_token(
    token: str,
) -> dict[str, Any] | None:
    return decode_jwt(token)


def create_invite_token(
    data: dict[str, Any],
) -> str:
    return generate_jwt(
        data=data,
        algorithm=settings.ALGORITHM,
        secret_key=settings.INVITE_TOKEN_SECRET_KEY,
        expires_delta=timedelta(minutes=settings.INVITE_TOKEN_EXPIRE_MINUTES),
    )


def decode_invite_token(
    token: str,
) -> dict[str, Any] | None:
    return decode_jwt(
        token, algorithm=settings.ALGORITHM, secret_key=settings.INVITE_TOKEN_SECRET_KEY
    )


def set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.AUTH_TOKEN_COOKIE_NAME,
        value=token,
        httponly=True,
        domain=settings.DOMAIN,
        secure=settings.ENVIRONMENT == Environment.PRODUCTION.value and True or False,
        samesite=settings.ENVIRONMENT == Environment.PRODUCTION.value
        and "None"
        or None,
        max_age=int(timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS).total_seconds()),
    )


def delete_auth_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.AUTH_TOKEN_COOKIE_NAME,
        domain=settings.DOMAIN,
    )
