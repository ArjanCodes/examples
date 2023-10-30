from typing import Any, Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

DATABASE_URL = "sqlite:///test.db"


class Base(DeclarativeBase):
    pass


class DatabaseService:
    def __init__(self) -> None:
        self.engine = create_engine(DATABASE_URL)
        self.session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Generator[Session, Any, Any]:
        database = self.session_local()
        try:
            yield database
        finally:
            database.close()
