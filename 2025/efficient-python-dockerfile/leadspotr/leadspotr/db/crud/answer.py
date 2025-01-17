from uuid import UUID

from sqlalchemy.orm import Session

from ...utils.logger import logger
from .. import models
from ..schemas.answer import Answer, AnswerCreate, AnswerUpdate


def get_answer_by_id(db: Session, id: UUID) -> Answer:
    return db.query(models.Answer).filter(models.Answer.id == id).first()


def get_answers_by_submission_id(db: Session, submission_id: UUID) -> list[Answer]:
    return (
        db.query(models.Answer)
        .filter(models.Answer.submission_id == submission_id)
        .all()
    )


def create_answer(db: Session, answer_create_input: AnswerCreate) -> Answer:
    db_answer = models.Answer(**answer_create_input.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    logger.info("Answer %s created successfully", db_answer.id)
    return db_answer


def update_answer(db: Session, id: UUID, answer: AnswerUpdate) -> Answer:
    db_answer = get_answer_by_id(db, id=id)
    for key, value in answer.dict(exclude_unset=True).items():
        setattr(db_answer, key, value)
    db.commit()
    db.refresh(db_answer)
    logger.info("Answer %s updated successfully", db_answer.id)
    return db_answer


def delete_answer(db: Session, id: UUID) -> Answer:
    db_answer = get_answer_by_id(db, id=id)
    db.delete(db_answer)
    db.commit()
    logger.info("Answer %s deleted successfully", db_answer.id)
    return db_answer
