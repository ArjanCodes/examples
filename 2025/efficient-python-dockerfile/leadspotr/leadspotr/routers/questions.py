from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import database
from ..db.crud.question import (
    create_question,
    delete_question,
    get_question_by_id,
    update_question,
)
from ..db.crud.question_option import create_question_option
from ..db.crud.quiz import get_quiz_by_id
from ..db.schemas.question import Question, QuestionCreate, QuestionUpdate
from ..db.schemas.question_option import QuestionOptionCreate
from ..db.schemas.user import User
from ..dependencies.authentication import get_current_user
from .router import APIRouter

router = APIRouter()

router.prefix = "/questions"


@router.get("/{id}", response_model=Question)
def get(
    id: UUID,
    db: Session = Depends(database.get_db),
) -> Question:
    db_question = get_question_by_id(db, id=id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@router.post("/", response_model=Question)
def create(
    question_create_input: QuestionCreate,
    db: Session = Depends(database.get_db),
    current_user: User | None = Depends(get_current_user),
) -> Question:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    db_quiz = get_quiz_by_id(
        db, id=question_create_input.quiz_id, user_id=current_user.id
    )

    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db_question = create_question(db=db, question_create_input=question_create_input)

    for _i in range(4):
        default_question_option = QuestionOptionCreate(
            question_id=db_question.id, text="", score=0
        )

        create_question_option(
            db=db, question_option_create_input=default_question_option
        )

    return db_question


@router.put("/{id}", response_model=Question)
def update(
    id: UUID,
    question_update_input: QuestionUpdate,
    db: Session = Depends(database.get_db),
    current_user: User | None = Depends(get_current_user),
) -> Question:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    db_question = get_question_by_id(db, id=id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db_quiz = get_quiz_by_id(db, id=db_question.quiz_id, user_id=current_user.id)

    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    update_question(db, id=id, question_update_input=question_update_input)
    return db_question


@router.delete("/{id}")
def delete(
    id: UUID,
    db: Session = Depends(database.get_db),
    current_user: User | None = Depends(get_current_user),
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    db_question = get_question_by_id(db, id=id)

    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db_quiz = get_quiz_by_id(db, id=db_question.quiz_id, user_id=current_user.id)

    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    delete_question(db, id=id)
    return {"status": 200, "message": "Question deleted"}
