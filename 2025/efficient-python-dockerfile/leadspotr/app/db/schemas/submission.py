from datetime import datetime
from enum import StrEnum, auto
from uuid import UUID

from humps import camelize
from pydantic import BaseModel

from .answer import Answer


class Tier(StrEnum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class SubmissionBase(BaseModel):
    quiz_slug: str
    email: str | None = None
    submitted_date: datetime | None = None
    score: int | None = None
    points: int | None = None
    tier: Tier | None = None


class SubmissionCreate(BaseModel):
    quiz_slug: str

    class Config:
        alias_generator = camelize
        populate_by_name = True


class SubmissionUpdate(BaseModel):
    email: str | None = None
    submitted_date: datetime | None = None
    score: int | None = None

    class Config:
        alias_generator = camelize
        populate_by_name = True


class Submission(SubmissionBase):
    id: UUID
    score: int | None = None
    answers: list[Answer] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        alias_generator = camelize
        populate_by_name = True
