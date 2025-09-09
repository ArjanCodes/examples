from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from typing import Generator

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)

# SQLite in-memory DB for demo purposes
engine = create_engine("sqlite:///:memory:", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    with db_session() as session:
        session.add_all([
            Article(id=1, title="Hello", body="World!"),
            Article(id=2, title="Python", body="Is Awesome"),
        ])
        session.commit()

@contextmanager
def db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()