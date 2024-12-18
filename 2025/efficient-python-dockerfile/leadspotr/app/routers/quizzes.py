from typing import Any
from uuid import UUID

from fastapi import Body, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..config import settings
from ..db import database
from ..db.crud.quiz import (
    create_quiz,
    delete_quiz,
    get_quiz_by_id,
    get_quiz_by_slug,
    update_quiz,
)
from ..db.schemas.image import Crop
from ..db.schemas.quiz import Quiz, QuizCreate, QuizUpdate
from ..db.schemas.user import User
from ..dependencies.authentication import get_current_user
from ..utils.file import delete_uploaded_file, upload_file
from ..utils.image import crop_image
from .router import APIRouter

router = APIRouter()

router.prefix = "/quizzes"


@router.post("/", response_model=Quiz)
async def create(
    quiz_create_input: QuizCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
) -> Quiz:
    return create_quiz(
        db=db, quiz_create_input=quiz_create_input, user_id=current_user.id
    )


@router.get("/{id}", response_model=Quiz)
async def get(
    id: UUID,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
) -> Quiz:
    if current_user is None:
        return None

    db_quiz = get_quiz_by_id(db, id=id, user_id=current_user.id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz


@router.get("/slug/{slug}", response_model=Quiz)
async def get_by_slug(
    slug: str,
    db: Session = Depends(database.get_db),
) -> Quiz:
    db_quiz = get_quiz_by_slug(db, slug=slug)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz


@router.put("/{id}", response_model=Quiz)
async def update(
    id: UUID,
    quiz_update_input: QuizUpdate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
) -> Quiz:
    db_quiz = get_quiz_by_id(db, id=id, user_id=current_user.id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    update_quiz(db, id=id, quiz_update_input=quiz_update_input, user_id=current_user.id)
    return db_quiz


@router.delete("/{id}")
async def delete(
    id: UUID,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    db_quiz = get_quiz_by_id(db, id=id, user_id=current_user.id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    delete_quiz(db, id, user_id=current_user.id)
    return {"status": 200, "message": f"Quiz {id} deleted successfully"}


# Background image endpoints

if settings.FEATURES["upload_file"]:

    @router.post("/{id}/background-image")
    def upload_background_image(
        id: UUID,
        crop: Crop = Body(...),
        background_image: UploadFile = File(...),
        db: Session = Depends(database.get_db),
        current_user: User = Depends(get_current_user),
    ) -> Quiz:
        db_quiz = get_quiz_by_id(db, id=id, user_id=current_user.id)
        if db_quiz is None:
            raise HTTPException(status_code=404, detail="Quiz not found")

        if db_quiz.background_image_url is not None:
            delete_uploaded_file(db_quiz.background_image_url)

        file_data = crop_image(image=background_image, crop=crop)

        if background_image.content_type is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        background_image_url = upload_file(
            file_data=file_data,
            content_type=background_image.content_type,
            folder_name="quiz-backgrounds",
        )

        update_data: dict[str, Any] = {"background_image_url": background_image_url}
        db_quiz = update_quiz(
            db,
            id=id,
            quiz_update_input=QuizUpdate(**update_data),
            user_id=current_user.id,
        )

        return db_quiz


if settings.FEATURES["upload_file"]:

    @router.delete("/{id}/background-image")
    def delete_background_image(
        id: UUID,
        db: Session = Depends(database.get_db),
        current_user: User = Depends(get_current_user),
    ) -> Quiz:
        db_quiz = get_quiz_by_id(db, id=id, user_id=current_user.id)
        if db_quiz is None:
            raise HTTPException(status_code=404, detail="Quiz not found")

        url = db_quiz.background_image_url
        delete_uploaded_file(url)

        # Update the background_image_url of the quiz to None
        update_data = {"background_image_url": None}
        db_quiz = update_quiz(
            db,
            id=id,
            quiz_update_input=QuizUpdate(**update_data),
            user_id=current_user.id,
        )

        return db_quiz
