from uuid import UUID

from sqlalchemy.orm import Session

from ...utils.logger import logger
from .. import models
from ..schemas.question import Question, QuestionCreate, QuestionUpdate


def get_question_by_id(db: Session, id: UUID) -> Question | None:
    return db.query(models.Question).filter(models.Question.id == id).first()


def create_question(db: Session, question_create_input: QuestionCreate) -> Question:
    db_question = models.Question(**question_create_input.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    logger.info("Question %s created successfully", db_question.id)
    return db_question


def update_question(
    db: Session,
    id: UUID,
    question_update_input: QuestionUpdate,
) -> Question | None:
    db_question = get_question_by_id(db, id=id)

    if db_question is None:
        raise ValueError(f"Question {id} not found")

    for attr, value in question_update_input.dict(exclude_unset=True).items():
        setattr(db_question, attr, value)
    db.commit()
    db.refresh(db_question)
    logger.info("Question %s updated successfully", db_question.id)

    return db_question


def delete_question(db: Session, id: UUID) -> None:
    db_question = get_question_by_id(db, id=id)
    # Delete all question options associated with the question
    db_question_options = db.query(models.QuestionOption).filter(
        models.QuestionOption.question_id == id
    )
    for db_question_option in db_question_options:
        db.delete(db_question_option)
    db_answers = db.query(models.Answer).filter(models.Answer.question_id == id)
    for db_answer in db_answers:
        db.delete(db_answer)
    db.delete(db_question)
    db.commit()
    logger.info("Question %s deleted successfully", id)
