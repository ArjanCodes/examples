import math

from sqlalchemy.orm import Session

from ..db.crud.answer import get_answers_by_submission_id
from ..db.crud.company import get_company_by_user_id
from ..db.crud.question_option import get_question_option_by_id
from ..db.crud.quiz import get_quiz_by_slug
from ..db.models import Answer, Quiz, Submission
from ..utils.generate_pdf import generate_pdf
from ..utils.logger import logger


def normalize_score(
    total_score: int, number_of_questions: int, max_answer_score: int
) -> int:
    return math.floor((total_score / (number_of_questions * max_answer_score)) * 100)


def compute_total_points(db: Session, db_answers: list[Answer]) -> int:
    return sum(
        get_question_option_by_id(db=db, id=db_answer.question_option_id).score
        for db_answer in db_answers
        if db_answer.question_option_id is not None
    )


def get_tier(score: int, quiz: Quiz) -> str:
    tier_map = {
        score < quiz.low_medium_cutoff: "low",
        score < quiz.medium_high_cutoff: "medium",
    }

    return tier_map.get(True, "high")


def compute_submission_score(db: Session, submission: Submission) -> Submission:
    db_answers = get_answers_by_submission_id(db, submission_id=submission.id)

    points = compute_total_points(db=db, db_answers=db_answers)
    submission.points = points

    logger.info("The total points for submission %s is %s", submission.id, points)

    score = normalize_score(
        total_score=points,
        number_of_questions=len(db_answers),
        max_answer_score=5,
    )

    logger.info("The normalized score for submission %s is %s", submission.id, score)

    submission.score = score

    db_quiz = get_quiz_by_slug(db, slug=submission.quiz_slug)
    submission.tier = get_tier(score=score, quiz=db_quiz)

    db.commit()
    db.refresh(submission)

    return submission


def generate_tier_pdf(db: Session, submission: Submission) -> str:
    db_quiz = get_quiz_by_slug(db, slug=submission.quiz_slug)
    db_company = get_company_by_user_id(db, user_id=db_quiz.user_id)

    tier_text_map = {
        "low": db_quiz.low_score_text,
        "medium": db_quiz.medium_score_text,
        "high": db_quiz.high_score_text,
    }
    tier_text = tier_text_map.get(submission.tier, db_quiz.high_score_text)

    output = f"Your Leadspotr Quiz Report.pdf"

    generate_pdf(html_string=tier_text, output=output, company_logo=db_company.logo_url)
    return output
