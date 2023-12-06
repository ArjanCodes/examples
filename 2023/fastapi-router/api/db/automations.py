from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .core import DBAutomation, NotFoundError


class Automation(BaseModel):
    id: int
    item_id: int
    code: str


class AutomationCreate(BaseModel):
    item_id: int
    code: str


class AutomationUpdate(BaseModel):
    item_id: Optional[int] = None
    code: Optional[str] = None


def read_db_automation(automation_id: int, session: Session) -> DBAutomation:
    db_automation = (
        session.query(DBAutomation).filter(DBAutomation.id == automation_id).first()
    )
    if db_automation is None:
        raise NotFoundError(f"Automation with id {automation_id} not found.")
    return db_automation


def create_db_automation(
    automation: AutomationCreate, session: Session
) -> DBAutomation:
    db_automation = DBAutomation(**automation.model_dump())
    session.add(db_automation)
    session.commit()
    session.refresh(db_automation)
    return db_automation


def update_db_automation(
    automation_id: int, automation: AutomationUpdate, session: Session
) -> DBAutomation:
    db_automation = read_db_automation(automation_id, session)
    for key, value in automation.model_dump(exclude_none=True).items():
        setattr(db_automation, key, value)
    session.commit()
    session.refresh(db_automation)
    return db_automation


def delete_db_automation(automation_id: int, session: Session) -> DBAutomation:
    db_automation = read_db_automation(automation_id, session)
    session.delete(db_automation)
    session.commit()
    return db_automation
