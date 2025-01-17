import os
from datetime import datetime
from uuid import UUID

from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..config import settings
from ..db import database
from ..db.crud.answer import create_answer
from ..db.crud.company import get_company_by_user_id
from ..db.crud.quiz import get_all_quizzes_by_user, get_quiz_by_id, get_quiz_by_slug
from ..db.crud.submission import (
    create_submission,
    delete_submission,
    get_all_submissions_by_quiz_slug,
    get_all_submissions_this_month_count,
    get_submission_by_id,
    update_submission,
)
from ..db.crud.user import get_user_by_id
from ..db.models import Quiz
from ..db.schemas.answer import AnswerCreate
from ..db.schemas.submission import Submission, SubmissionCreate, SubmissionUpdate
from ..db.schemas.user import User
from ..dependencies.authentication import get_current_user
from ..email import email_client
from ..email.attachment import SendGridAttachmentWrapper
from ..utils.file import encode_file_to_base64
from ..utils.submission import compute_submission_score, generate_tier_pdf
from .router import APIRouter

router = APIRouter()

router.prefix = "/submissions"


def has_reached_submission_limit(db: Session, user_id: UUID) -> bool:
    db_user = get_user_by_id(db, id=user_id)
    db_company = get_company_by_user_id(db, user_id=db_user.id)
    submissions_this_month_count = get_all_submissions_this_month_count(
        db=db, user_id=db_user.id
    )

    if submissions_this_month_count >= db_company.submissions_cap:
        return True

    return False


def create_answer_for_submission(db: Session, quiz: Quiz, submission_id: UUID) -> None:
    db_questions = quiz.questions

    # Create answers for submission
    for question in db_questions:
        # Create answer create input dict with question id and submission id
        answer_create_input = AnswerCreate(
            question_id=question.id, submission_id=submission_id
        )

        create_answer(db=db, answer_create_input=answer_create_input)


@router.post("/", response_model=Submission)
def create(
    create_submission_input: SubmissionCreate,
    db: Session = Depends(database.get_db),
) -> Submission:
    db_quiz = get_quiz_by_slug(db, slug=create_submission_input.quiz_slug)

    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Check if company submission cap is reached for this month
    if has_reached_submission_limit(db, user_id=db_quiz.user_id):
        raise HTTPException(
            status_code=403,
            detail="You have reached your submission limit for this month",
        )

    db_submission = create_submission(
        db=db, create_submission_input=create_submission_input
    )

    create_answer_for_submission(db, quiz=db_quiz, submission_id=db_submission.id)

    return db_submission


@router.get("/", response_model=list[Submission])
def get_all_by_quiz_id(
    quiz_id: UUID = Query(..., alias="quizId"),
    session: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
) -> list[Submission]:
    db_quiz = get_quiz_by_id(session, id=quiz_id, user_id=current_user.id)

    return get_all_submissions_by_quiz_slug(session, quiz_slug=db_quiz.slug)


@router.get("/{id}", response_model=Submission)
def get(
    id: UUID,
    db: Session = Depends(database.get_db),
) -> Submission:
    db_submission = get_submission_by_id(db, id=id)
    if db_submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    return db_submission


@router.post("/{id}", response_model=Submission)
def submit(
    id: str,
    update_submission_input: SubmissionUpdate,
    db: Session = Depends(database.get_db),
) -> Submission:
    db_submission = get_submission_by_id(db, id=id)
    if db_submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")

    update_submission_input.submitted_date = datetime.now()
    db_submission = update_submission(
        db,
        id=id,
        update_submission_input=update_submission_input,
    )

    # Update score
    compute_submission_score(db, submission=db_submission)

    # Generate PDF
    file_path = generate_tier_pdf(db, submission=db_submission)

    encoded_attachment = encode_file_to_base64(file_path)
    attachment = SendGridAttachmentWrapper(
        file_content=encoded_attachment,
        file_name=file_path,
        file_type="application/pdf",
        disposition="attachment",
    )

    data = {
        "attachment_base64": encoded_attachment,
        "attachment_mime_type": "application/pdf",
        "attachment_url": file_path,
    }

    # Send email with PDF
    email_client.send_mail(
        recipients=[db_submission.email],
        subject="Your quiz results!",
        data=data,
        template_id=settings.SENDGRID_TIER_PDF_TEMPLATE_ID,
        attachments=[attachment],
    )

    # Delete PDF after sending
    if os.path.exists(file_path):
        os.remove(file_path)

    return db_submission


@router.delete("/{id}")
def delete(
    id: UUID,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    db_submission = get_submission_by_id(db, id=id)

    if db_submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")

    db_quizzes = get_all_quizzes_by_user(db, user_id=current_user.id)
    if db_submission.quiz_slug not in [quiz.slug for quiz in db_quizzes]:
        raise HTTPException(status_code=403, detail="Forbidden")

    delete_submission(db, id=id)
    return {"status": 200, "message": "Submission deleted"}
