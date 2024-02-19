from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel


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


class Base(DeclarativeBase):
    pass


class DBItem(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]]


def db_find_item(item_id: int, db: Session) -> DBItem:
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise NotFoundError()
    return db_item


def db_create_item(item: ItemCreate, session: Session) -> Item:
    db_item = DBItem(**item.model_dump())
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return Item(**db_item.__dict__)


def db_read_item(item_id: int, session: Session) -> Item:
    db_item = db_find_item(item_id, session)
    return Item(**db_item.__dict__)


def db_update_item(item_id: int, session: Session) -> Item:
    db_item = db_find_item(item_id, session)

    for key, value in db_item.__dict__.items():
        setattr(db_item, key, value)

    session.commit()
    session.refresh(db_item)

    return Item(**db_item.__dict__)


def db_delete_item(item_id: int, session: Session) -> Item:
    db_item = db_find_item(item_id, session)
    session.delete(db_item)
    session.commit()
    return Item(**db_item.__dict__)
