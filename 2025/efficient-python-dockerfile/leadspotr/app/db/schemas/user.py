from datetime import datetime
from uuid import UUID

from humps import camelize
from pydantic import BaseModel

from ..models import RoleEnum
from .company import Company
from .quiz import Quiz


class UserBase(BaseModel):
    email: str
    name: str
    active: bool = False


class UserCreate(UserBase):
    company_id: UUID
    hashed_password: str | None = None
    role: RoleEnum = RoleEnum.user

    class Config:
        alias_generator = camelize
        populate_by_name = True


class UserUpdate(BaseModel):
    name: str
    email: str | None = None
    active: bool | None = None

    class Config:
        alias_generator = camelize
        populate_by_name = True


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        alias_generator = camelize
        populate_by_name = True


class UserInviteInput(BaseModel):
    email: str

    class Config:
        alias_generator = camelize
        populate_by_name = True


class UserRegister(UserBase):
    company_name: str
    password: str | None = None

    class Config:
        alias_generator = camelize
        populate_by_name = True


class User(UserBase):
    id: UUID
    company: Company | None
    quizzes: list[Quiz] = []
    created_at: datetime
    updated_at: datetime
    role: RoleEnum = RoleEnum.user

    class Config:
        from_attributes = True
        alias_generator = camelize
        populate_by_name = True
