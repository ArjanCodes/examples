from datetime import datetime
from uuid import UUID

from humps import camelize
from pydantic import BaseModel

from .question_option import QuestionOption


class QuestionBase(BaseModel):
    text: str | None = None


class QuestionCreate(QuestionBase):
    quiz_id: UUID

    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class QuestionUpdate(QuestionBase):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class Question(QuestionBase):
    id: UUID
    quiz_id: UUID
    options: list[QuestionOption] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        alias_generator = camelize
        allow_population_by_field_name = True
