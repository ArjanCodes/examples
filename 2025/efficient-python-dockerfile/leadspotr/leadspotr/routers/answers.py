from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import database
from ..db.crud.answer import get_answer_by_id, update_answer
from ..db.schemas.answer import Answer, AnswerUpdate
from .router import APIRouter

router = APIRouter()

router.prefix = "/answers"


@router.put("/{id}", response_model=Answer)
def update(
    id: UUID,
    answer: AnswerUpdate,
    db: Session = Depends(database.get_db),
) -> Answer:
    db_answer = get_answer_by_id(db, id=id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")

    update_answer(
        db,
        id=id,
        answer=answer,
    )
    return db_answer
