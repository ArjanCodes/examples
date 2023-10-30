from typing import Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, Session
from .core import Base


class NotFoundError(Exception):
    pass


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str]


class ItemCreate(BaseModel):
    name: str
    description: Optional[str]


class ItemUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]


class DBItem(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]]


def read_db_item(item_id: int, session: Session) -> DBItem:
    db_item = session.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise NotFoundError(f"Item with id {item_id} not found.")
    return db_item


def create_db_item(item: ItemCreate, session: Session) -> DBItem:
    db_item = DBItem(**item.model_dump())
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def update_db_item(item_id: int, item: ItemUpdate, session: Session) -> DBItem:
    db_item = read_db_item(item_id, session)
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    session.commit()
    session.refresh(db_item)
    return db_item


def delete_db_item(item_id: int, session: Session) -> DBItem:
    db_item = read_db_item(item_id, session)
    session.delete(db_item)
    session.commit()
    return db_item
