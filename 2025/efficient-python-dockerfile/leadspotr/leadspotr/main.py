from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import AuthProviders, settings

# from app.db import database, models
from app.routers import (
    answers,
    auth_github,
    auth_passwordless,
    auth_with_email_password,
    companies,
    question_options,
    questions,
    quizzes,
    submissions,
    users,
)
from app.utils.logger import setup_logger

# models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(docs_url=settings.DOCS_URL, redoc_url=settings.REDOC_URL)

origins = [settings.FRONTEND_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_logger()


@app.get("/")
async def health_check() -> str:
    return "Server is running"


auth_providers = settings.AUTH_PROVIDERS


if AuthProviders.PASSWORDLESS.value in auth_providers:
    app.include_router(auth_passwordless.router)
if AuthProviders.GITHUB.value in auth_providers:
    app.include_router(auth_github.router)
if AuthProviders.WITH_EMAIL_PASSWORD.value in auth_providers:
    app.include_router(auth_with_email_password.router)

app.include_router(users.router)
app.include_router(companies.router)
app.include_router(quizzes.router)
app.include_router(questions.router)
app.include_router(question_options.router)
app.include_router(answers.router)
app.include_router(submissions.router)
