from sqlalchemy import Column, DateTime, MetaData, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from ..config import Environment, settings
from .connectors import connect_to_db, connect_to_local_db

engine, SessionLocal = (
    connect_to_db()
    if settings.ENVIRONMENT == Environment.PRODUCTION.value
    else connect_to_local_db()
)


metadata_obj = MetaData(schema="leadspotr")
dec_base = declarative_base(metadata=metadata_obj)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(dec_base):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
