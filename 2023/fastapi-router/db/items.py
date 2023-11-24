from typing import Optional
from automation.run import run_automations
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .core import DBAutomation, DBItem, NotFoundError


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


def read_db_item(item_id: int, session: Session) -> DBItem:
    db_item = session.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise NotFoundError(f"Item with id {item_id} not found.")
    return db_item


def read_db_automations_for_item(item_id: int, session: Session) -> list[DBAutomation]:
    return session.query(DBAutomation).filter(DBAutomation.item_id == item_id).all()


def create_db_item(item: ItemCreate, session: Session) -> DBItem:
    db_item = DBItem(**item.model_dump(exclude_none=True))
    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


def update_db_item(item_id: int, item: ItemUpdate, session: Session) -> DBItem:
    db_item = read_db_item(item_id, session)
    for key, value in item.model_dump(exclude_none=True).items():
        setattr(db_item, key, value)
    session.commit()
    session.refresh(db_item)

    # get the automations
    automations = read_db_automations_for_item(db_item.id, session)
    run_automations(automations)

    return db_item


def delete_db_item(item_id: int, session: Session) -> DBItem:
    db_item = read_db_item(item_id, session)
    session.delete(db_item)
    session.commit()
    return db_item
