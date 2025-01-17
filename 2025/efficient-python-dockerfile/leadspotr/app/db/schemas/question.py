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
        populate_by_name = True


class QuestionUpdate(QuestionBase):
    class Config:
        alias_generator = camelize
        populate_by_name = True


class Question(QuestionBase):
    id: UUID
    quiz_id: UUID
    options: list[QuestionOption] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        alias_generator = camelize
        populate_by_name = True
