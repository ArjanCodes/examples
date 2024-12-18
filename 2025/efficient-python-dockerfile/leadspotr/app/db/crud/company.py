from uuid import UUID

from sqlalchemy.orm import Session

from ...utils.logger import logger
from .. import models
from ..schemas.company import Company, CompanyCreate, CompanyUpdate


def get_company_by_user_id(db: Session, user_id: UUID | None = None) -> Company | None:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        return None

    db_company = (
        db.query(models.Company).filter(models.Company.id == db_user.company_id).first()
    )
    if not db_company:
        return None

    return db_company


def create_company(db: Session, company: CompanyCreate) -> Company:
    db_company = models.Company(name=company.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    logger.info("Company %s created successfully", db_company.id)
    return db_company


def update_company(
    db: Session, user_id: UUID, company: CompanyUpdate
) -> Company | None:
    db_company = get_company_by_user_id(db, user_id=user_id)

    if not db_company:
        return None

    for key, value in company.dict(exclude_unset=True).items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    logger.info("Company %s updated successfully", db_company.id)
    return db_company


def delete_company(db: Session, user_id: UUID) -> Company | None:
    db_company = get_company_by_user_id(db, user_id=user_id)

    if not db_company:
        return None

    db.delete(db_company)
    db.commit()
    logger.info("Company %s deleted successfully", db_company.id)
    return db_company
