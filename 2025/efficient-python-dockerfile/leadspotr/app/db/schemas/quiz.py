from datetime import datetime
from uuid import UUID

from humps import camelize
from pydantic import BaseModel

from .question import Question


class QuizBase(BaseModel):
    title: str | None
    slug: str | None = None
    introduction: str | None = None
    show_company_logo: bool = False
    background_image_url: str | None = None
    main_color: str | None = None
    low_score_text: str | None = None
    medium_score_text: str | None = None
    high_score_text: str | None = None
    low_medium_cutoff: int | None = None
    medium_high_cutoff: int | None = None


class QuizCreate(BaseModel):
    title: str | None = None

    class Config:
        alias_generator = camelize
        populate_by_name = True


class QuizUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    introduction: str | None = None
    show_company_logo: bool | None = False
    background_image_url: str | None = None
    main_color: str | None = None
    low_score_text: str | None = None
    medium_score_text: str | None = None
    high_score_text: str | None = None
    low_medium_cutoff: int | None = None
    medium_high_cutoff: int | None = None

    class Config:
        alias_generator = camelize
        populate_by_name = True


class Quiz(QuizBase):
    id: UUID
    questions: list[Question] = []
    created_at: datetime
    updated_at: datetime
    company_logo_url: str | None | None = None

    class Config:
        from_attributes = True
        alias_generator = camelize
        populate_by_name = True
