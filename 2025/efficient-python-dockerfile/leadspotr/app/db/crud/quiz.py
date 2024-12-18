from typing import Sequence
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from ...utils.logger import logger
from .. import models
from ..crud.company import get_company_by_user_id
from ..crud.question import delete_question
from ..schemas.quiz import Quiz, QuizCreate, QuizUpdate


def get_quiz_by_id(db: Session, id: UUID, user_id: UUID) -> Quiz | None:
    # Check if the quiz belongs to the user
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()

    if db_quiz or db_user is None:
        return None

    if db_quiz.user_id != db_user.id:
        raise Exception("You do not have permission to view this quiz")

    db_company = get_company_by_user_id(db, user_id=db_user.id)
    db_quiz.company_logo_url = db_company.logo_url

    return db_quiz


def get_quiz_by_slug(db: Session, slug: str) -> Quiz | None:
    db_quiz = db.query(models.Quiz).filter(models.Quiz.slug == slug).first()

    # Retrieve the company logo
    db_user = db.query(models.User).filter(models.User.id == db_quiz.user_id).first()
    db_company = get_company_by_user_id(db, user_id=db_user.id)
    db_quiz.company_logo_url = db_company.logo_url

    return db_quiz


def get_all_quizzes_by_user(
    db: Session, user_id: UUID, skip: int = 0, limit: int = 100
) -> Sequence[Quiz]:
    return (
        db.query(models.Quiz)
        .filter(models.Quiz.user_id == user_id)
        .order_by(models.Quiz.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_all_quizzes(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Quiz]:
    return (
        db.query(models.Quiz).order_by(models.Quiz.id).offset(skip).limit(limit).all()
    )


def create_quiz(
    db: Session, quiz_create_input: QuizCreate, user_id: UUID
) -> Quiz | None:
    # Check if the user has reached their quiz cap
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if db_user is None:
        return None

    db_company = (
        db.query(models.Company).filter(models.Company.id == db_user.company_id).first()
    )

    if db_company is None:
        return None

    if len(db_user.quizzes) >= db_company.quizzes_cap:
        logger.error("User %s has reached their quiz cap", db_user.id)
        raise Exception("You have reached your quiz cap")

    db_quiz = models.Quiz(**quiz_create_input.dict(), user_id=user_id)
    # Generate a slug for the quiz
    db_quiz.slug = (
        f"{quiz_create_input.title.lower().replace(' ', '_')}_{uuid4().hex[:6]}"
    )
    db.add(db_quiz)
    # Reduce the user's quiz cap by 1
    db_company.quizzes_cap -= 1

    db.commit()
    db.refresh(db_quiz)
    db.refresh(db_company)
    logger.info("Quiz %s created successfully", db_quiz.id)
    return db_quiz


def update_quiz(
    db: Session, id: UUID, quiz_update_input: QuizUpdate, user_id: UUID
) -> Quiz:
    # Check if quiz belongs to user
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_quiz = get_quiz_by_id(db, id=id, user_id=user_id)

    if db_quiz is None:
        raise Exception("Quiz not found")

    if db_quiz.user_id != db_user.id:
        logger.error(
            "User %s does not have permission to update quiz %s", db_user.id, db_quiz.id
        )
        raise Exception("You do not have permission to update this quiz")

    for attr, value in quiz_update_input.dict(exclude_unset=True).items():
        setattr(db_quiz, attr, value)
    db.commit()
    db.refresh(db_quiz)
    logger.info("Quiz %s updated successfully", db_quiz.id)
    return db_quiz


def delete_quiz(db: Session, id: UUID, user_id: UUID) -> Quiz:
    # Check if quiz belongs to user
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_quiz = get_quiz_by_id(db, id=id, user_id=user_id)

    if db_quiz is None:
        raise Exception("Quiz not found")

    if db_quiz.user_id != db_user.id:
        logger.error(
            "User %s does not have permission to delete quiz %s", db_user.id, db_quiz.id
        )
        raise Exception("You do not have permission to delete this quiz")

    db.delete(db_quiz)
    # Delete all questions associated with the quiz
    db_questions = db.query(models.Question).filter(models.Question.quiz_id == id).all()
    for db_question in db_questions:
        delete_question(db, id=db_question.id)

    # Increase the user's quiz cap by 1
    db_company = (
        db.query(models.Company).filter(models.Company.id == db_user.company_id).first()
    )
    db_company.quizzes_cap += 1

    db.commit()
    db.refresh(db_company)
    logger.info("Quiz %s deleted successfully", db_quiz.id)
    return db_quiz
