import uuid

from sqlalchemy.orm import Session

from ...utils.logger import logger
from .. import models
from ..schemas.user import User, UserCreate, UserUpdate


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return (
        db.query(models.User).order_by(models.User.id).offset(skip).limit(limit).all()
    )


def get_users_by_company_id(db: Session, company_id: uuid.UUID) -> list[User]:
    return db.query(models.User).filter(models.User.company_id == company_id).all()


def get_user_by_id(db: Session, id: uuid.UUID) -> User | None:
    return db.query(models.User).filter(models.User.id == id).first()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = models.User(**user.dict(exclude_unset=True))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info("User %s created successfully", db_user.id)
    return db_user


def update_user(db: Session, id: uuid.UUID, user: UserUpdate) -> User:
    db_user = get_user_by_id(db, id=id)
    for attr, value in user.dict(exclude_unset=True).items():
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    logger.info("User %s updated successfully", db_user.id)
    return db_user
