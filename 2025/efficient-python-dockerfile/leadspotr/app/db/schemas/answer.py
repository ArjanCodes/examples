from datetime import datetime
from uuid import UUID

from humps import camelize
from pydantic import BaseModel


class AnswerBase(BaseModel):
    pass


class AnswerCreate(AnswerBase):
    submission_id: UUID
    question_id: UUID

    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class AnswerUpdate(AnswerBase):
    question_option_id: UUID | None = None

    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class Answer(AnswerBase):
    id: UUID
    question_id: UUID
    question_option_id: UUID | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        alias_generator = camelize
        allow_population_by_field_name = True
