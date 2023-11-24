from typing import Optional
from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from .core import Base, NotFoundError
from .items import Item


class Automation(BaseModel):
    id: int
    item_id: int
    code: str


class AutomationCreate(BaseModel):
    item_id: int
    code: str


class AutomationUpdate(BaseModel):
    item_id: Optional[int]
    code: Optional[str]


class DBAutomation(Base):
    __tablename__ = "automations"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    item: Mapped[Item] = relationship()
    code: Mapped[str]


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
    for key, value in automation.model_dump().items():
        setattr(db_automation, key, value)
    session.commit()
    session.refresh(db_automation)
    return db_automation


def delete_db_automation(automation_id: int, session: Session) -> DBAutomation:
    db_automation = read_db_automation(automation_id, session)
    session.delete(db_automation)
    session.commit()
    return db_automation
