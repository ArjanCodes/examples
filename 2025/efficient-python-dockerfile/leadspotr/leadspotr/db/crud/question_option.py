import uuid
from typing import Sequence

from sqlalchemy.orm import Session

from ...utils.logger import logger
from .. import models
from ..crud.question import get_question_by_id
from ..schemas.question_option import (
    QuestionOption,
    QuestionOptionCreate,
    QuestionOptionUpdate,
)


def get_question_option_by_id(db: Session, id: uuid.UUID) -> QuestionOption:
    return (
        db.query(models.QuestionOption).filter(models.QuestionOption.id == id).first()
    )


def get_question_option_by_question_id(
    db: Session, question_id: uuid.UUID
) -> Sequence[QuestionOption]:
    return (
        db.query(models.QuestionOption)
        .filter(models.QuestionOption.question_id == question_id)
        .order_by(models.QuestionOption.id)
        .all()
    )


def create_question_option(
    db: Session, question_option_create_input: QuestionOptionCreate
) -> QuestionOption | None:
    db_question = get_question_by_id(db, id=question_option_create_input.question_id)
    if db_question is None:
        return None
    db_question_option = models.QuestionOption(
        id=uuid.uuid4(), **question_option_create_input.dict()
    )
    db_question_option.position = len(db_question.options)
    db.add(db_question_option)
    db.commit()
    db.refresh(db_question_option)
    logger.info("QuestionOption %s created successfully", db_question_option.id)
    return db_question_option


def update_question_option(
    db: Session,
    id: uuid.UUID,
    question_option_update_input: QuestionOptionUpdate,
) -> QuestionOption:
    db_question_option = get_question_option_by_id(db, id=id)
    for key, value in question_option_update_input.dict(exclude_unset=True).items():
        setattr(db_question_option, key, value)
    db.commit()
    db.refresh(db_question_option)
    logger.info("QuestionOption %s updated successfully", db_question_option.id)
    return db_question_option


def update_question_option_position(
    db: Session,
    id: uuid.UUID,
    new_position: int,
) -> QuestionOption:
    db_question_option = get_question_option_by_id(db, id=id)
    current_position = db_question_option.position
    if current_position == new_position:
        return db_question_option
    if current_position < new_position:
        db_question_effected_options = (
            db.query(models.QuestionOption)
            .filter(
                models.QuestionOption.question_id == db_question_option.question_id,
                models.QuestionOption.position > current_position,
                models.QuestionOption.position <= new_position,
            )
            .all()
        )
        for db_question_effected_option in db_question_effected_options:
            db_question_effected_option.position -= 1
    else:
        db_question_effected_options = (
            db.query(models.QuestionOption)
            .filter(
                models.QuestionOption.question_id == db_question_option.question_id,
                models.QuestionOption.position >= new_position,
                models.QuestionOption.position < current_position,
            )
            .all()
        )
        for db_question_effected_option in db_question_effected_options:
            db_question_effected_option.position += 1

    db_question_option.position = new_position
    db.commit()
    db.refresh(db_question_option)
    logger.info("QuestionOption %s updated successfully", db_question_option.id)
    return db_question_option


def delete_question_option(db: Session, id: uuid.UUID) -> QuestionOption | None:
    db_question_option = get_question_option_by_id(db, id=id)
    db_question = get_question_by_id(db, id=db_question_option.question_id)
    if db_question is None:
        raise ValueError(f"Question {db_question_option.question_id} not found")

    db_question_effected_options = (
        db.query(models.QuestionOption)
        .filter(
            models.QuestionOption.question_id == db_question_option.question_id,
            models.QuestionOption.position > db_question_option.position,
        )
        .all()
    )

    for db_question_effected_option in db_question_effected_options:
        db_question_effected_option.position -= 1

    db.delete(db_question_option)
    db.commit()
    logger.info("QuestionOption %s deleted successfully", db_question_option.id)
    return db_question_option
