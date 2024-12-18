from datetime import datetime
from typing import Any
from uuid import UUID

from humps import camelize
from pydantic import BaseModel, validator

MIN = 0
MAX = 5


class QuestionOptionBase(BaseModel):
    text: str | None = None
    score: int = 0

    @validator("score")
    def score_range(cls, v: Any) -> Any:
        if v < MIN or v > MAX:
            raise ValueError(f"score must be between {MIN} and {MAX}")
        return v


class QuestionOptionCreate(QuestionOptionBase):
    question_id: UUID

    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class QuestionOptionUpdate(QuestionOptionBase):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class QuestionOptionPositionUpdate(BaseModel):
    position: int

    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class QuestionOption(QuestionOptionBase):
    id: UUID
    question_id: UUID
    created_at: datetime
    updated_at: datetime
    position: int

    class Config:
        orm_mode = True
        alias_generator = camelize
        allow_population_by_field_name = True
