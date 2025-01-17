import uuid
from datetime import datetime

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from ...utils.logger import logger
from .. import models
from ..crud.quiz import get_all_quizzes_by_user
from ..schemas.submission import Submission, SubmissionCreate, SubmissionUpdate


def get_submission_by_id(db: Session, id: uuid.UUID) -> Submission:
    return db.query(models.Submission).filter(models.Submission.id == id).first()


def get_submission_by_quiz_slug(db: Session, slug: str) -> Submission:
    return (
        db.query(models.Submission).filter(models.Submission.quiz_slug == slug).first()
    )


def get_all_submissions_by_quiz_slug(db: Session, quiz_slug: str) -> list[Submission]:
    return (
        db.query(models.Submission)
        .filter(
            and_(
                models.Submission.quiz_slug == quiz_slug,
                models.Submission.submitted_date is not None,
            )
        )
        .order_by(models.Submission.id)
        .all()
    )


def create_submission(
    db: Session, create_submission_input: SubmissionCreate
) -> Submission:
    db_submission = models.Submission(quiz_slug=create_submission_input.quiz_slug)
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    logger.info("Submission %s created successfully", db_submission.id)
    return db_submission


def update_submission(
    db: Session, id: uuid.UUID, update_submission_input: SubmissionUpdate
) -> Submission:
    db_submission = get_submission_by_id(db, id=id)
    for key, value in update_submission_input.dict(exclude_unset=True).items():
        setattr(db_submission, key, value)
    db.commit()
    db.refresh(db_submission)
    logger.info("Submission %s updated successfully", db_submission.id)
    return db_submission


def delete_submission(db: Session, id: uuid.UUID) -> bool:
    db_submission = get_submission_by_id(db, id=id)
    if db_submission:
        db.delete(db_submission)
        db.commit()
        logger.info("Submission %s deleted successfully", db_submission.id)
        return True
    return False


def get_all_submissions_this_month_count(db: Session, user_id: uuid.UUID) -> int:
    quizzes = get_all_quizzes_by_user(db, user_id=user_id)

    def is_this_month(date):
        now = datetime.now()
        month = func.extract("month", date)
        year = func.extract("year", date)
        return and_(month == now.month, year == now.year)

    return (
        db.query(func.count(models.Submission.id))
        .filter(
            models.Submission.quiz_slug.in_([quiz.slug for quiz in quizzes]),
            is_this_month(models.Submission.created_at),
            models.Submission.submitted_date is not None,
        )
        .scalar()
    )
