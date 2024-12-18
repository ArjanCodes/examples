from datetime import datetime
from uuid import UUID

from humps import camelize
from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    website: str | None = None
    logo_url: str | None = None
    stripe_customer_id: str | None = None
    api_key: str | None = None
    api_secret: str | None = None
    quizzes_cap: int = 5
    submissions_cap: int = 10
    invite_code: str | None = None


class CompanyCreate(BaseModel):
    name: str

    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class CompanyUpdate(BaseModel):
    name: str | None = None
    website: str | None = None
    logo_url: str | None = None
    stripe_customer_id: str | None = None
    api_key: str | None = None
    api_secret: str | None = None
    invite_code: str | None = None

    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class Company(CompanyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        alias_generator = camelize
        allow_population_by_field_name = True
