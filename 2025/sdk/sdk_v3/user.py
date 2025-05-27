from typing import ClassVar

from pydantic import EmailStr

from .base import BaseAPIModel


class User(BaseAPIModel["User"]):
    name: str
    email: EmailStr

    _resource_path: ClassVar[str] = "users"
