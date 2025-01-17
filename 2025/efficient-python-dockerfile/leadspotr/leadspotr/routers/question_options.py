from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import database
from ..db.crud.question import get_question_by_id
from ..db.crud.question_option import (
    create_question_option,
    delete_question_option,
    get_question_option_by_id,
    update_question_option,
    update_question_option_position,
)
from ..db.crud.quiz import get_quiz_by_id
from ..db.schemas.question_option import (
    QuestionOption,
    QuestionOptionCreate,
    QuestionOptionPositionUpdate,
    QuestionOptionUpdate,
)
from ..db.schemas.user import User
from ..dependencies.authentication import get_current_user
from .router import APIRouter

router = APIRouter()

router.prefix = "/question-options"


@router.get("/{id}", response_model=QuestionOption)
def get(
    id: UUID,
    db: Session = Depends(database.get_db),
) -> QuestionOption:
    db_question_option = get_question_option_by_id(db, id=id)
    if db_question_option is None:
        raise HTTPException(status_code=404, detail="Question option not found")
    return db_question_option


@router.post("/", response_model=QuestionOption)
def create(
    question_option_create_input: QuestionOptionCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
) -> QuestionOption:
    db_question = get_question_by_id(db, id=question_option_create_input.question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db_quiz = get_quiz_by_id(db, id=db_question.quiz_id, user_id=current_user.id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db_question_option = create_question_option(
        db=db, question_option_create_input=question_option_create_input
    )

    return db_question_option


@router.put("/{id}", response_model=QuestionOption)
def update(
    id: UUID,
    question_option_update_input: QuestionOptionUpdate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
) -> QuestionOption:
    db_question_option = get_question_option_by_id(db, id=id)
    if db_question_option is None:
        raise HTTPException(status_code=404, detail="Question option not found")

    db_question = get_question_by_id(db, id=db_question_option.question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db_quiz = get_quiz_by_id(db, id=db_question.quiz_id, user_id=current_user.id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    update_question_option(
        db,
        id=id,
        question_option_update_input=question_option_update_input,
    )
    return db_question_option


@router.put("/{id}/move-to-position", response_model=QuestionOption)
def move_to(
    id: UUID,
    question_option_update_input: QuestionOptionPositionUpdate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
) -> QuestionOption:
    db_question_option = get_question_option_by_id(db, id=id)
    if db_question_option is None:
        raise HTTPException(status_code=404, detail="Question option not found")

    db_question = get_question_by_id(db, id=db_question_option.question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db_quiz = get_quiz_by_id(db, id=db_question.quiz_id, user_id=current_user.id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    update_question_option_position(
        db,
        id=id,
        new_position=question_option_update_input.position,
    )
    return db_question_option


@router.delete("/{id}")
def delete(
    id: UUID,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    db_question_option = get_question_option_by_id(db, id=id)
    if db_question_option is None:
        raise HTTPException(status_code=404, detail="Question option not found")

    db_question = get_question_by_id(db, id=db_question_option.question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db_quiz = get_quiz_by_id(db, id=db_question.quiz_id, user_id=current_user.id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    delete_question_option(db, id=id)
    return {"status": 200, "message": "Question option deleted"}
