import uuid
from enum import Enum, unique

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base


@unique
class RoleEnum(Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))
    role = Column(
        pgEnum(RoleEnum, name="role", inherit_schema=True), default=RoleEnum.user
    )
    hashed_password = Column(String, nullable=True)
    active = Column(Boolean, default=True)

    company = relationship("Company", back_populates="users")
    quizzes = relationship("Quiz", back_populates="user", order_by="Quiz.created_at")


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    website = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    stripe_customer_id = Column(String, nullable=True)
    api_key = Column(String, nullable=True)
    api_secret = Column(String, nullable=True)
    quizzes_cap = Column(Integer, nullable=True, default=5)
    submissions_cap = Column(Integer, nullable=True, default=10)
    invite_code = Column(String, nullable=True)

    users = relationship("User", back_populates="company")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    slug = Column(String, unique=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    introduction = Column(String, nullable=True)
    show_company_logo = Column(Boolean, default=False)
    background_image_url = Column(String, nullable=True)
    main_color = Column(String, nullable=True)
    low_score_text = Column(String, nullable=True, default="<h1>Low score text</h1>")
    medium_score_text = Column(
        String, nullable=True, default="<h1>Medium score text</h1>"
    )
    high_score_text = Column(String, nullable=True, default="<h1>High score text</h1>")
    low_medium_cutoff = Column(Integer, nullable=True, default=30)
    medium_high_cutoff = Column(Integer, nullable=True, default=70)

    user = relationship("User", back_populates="quizzes")
    questions = relationship(
        "Question", back_populates="quiz", order_by="Question.created_at"
    )
    submissions = relationship(
        "Submission", back_populates="quiz", order_by="Submission.updated_at"
    )


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String, nullable=True)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship(
        "QuestionOption", back_populates="question", order_by="QuestionOption.position"
    )


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String, nullable=True)
    score = Column(Integer)
    position = Column(Integer, nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))

    question = relationship("Question", back_populates="options")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String)
    quiz_slug = Column(String, ForeignKey("quizzes.slug"))
    score = Column(Integer)
    points = Column(Integer)
    tier = Column(String, nullable=True)
    submitted_date = Column(DateTime, nullable=True)

    quiz = relationship("Quiz", back_populates="submissions")
    answers = relationship("Answer", back_populates="submission")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_option_id = Column(UUID(as_uuid=True), nullable=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id"))

    submission = relationship("Submission", back_populates="answers")


# Indexes for various columns

# Index for User table on company_id column
Index("users_company_id_idx", User.company_id)

# Index for Quiz table on user_id column
Index("quizzes_user_id_idx", Quiz.user_id)

# Index for Submission table on quiz_id column
Index("submissions_quiz_slug_idx", Submission.quiz_slug)

# Index for Submission table on email column
Index("submissions_email_idx", Submission.email)

# Index for Answer table on submission_id column
Index("answers_submission_id_idx", Answer.submission_id)

# Index for Answer table on question_id column
Index("answers_question_id_idx", Answer.question_id)

# Index for QuestionOption table on question_id column
Index("question_options_question_id_idx", QuestionOption.question_id)

# Index for Question table on quiz_id column
Index("questions_quiz_id_idx", Question.quiz_id)
