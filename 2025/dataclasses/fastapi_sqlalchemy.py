import secrets

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)

# --- Database setup ---

DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False)


# declarative base class
class Base(DeclarativeBase):
    pass


# --- SQLAlchemy ORM model ---


class Book(Base):
    __tablename__ = "books"

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: secrets.token_hex(12)
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    pages: Mapped[int] = mapped_column(Integer, default=0)


# --- Pydantic models ---


class BookCreate(BaseModel):
    title: str
    author: str
    pages: int = 0


class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    pages: int

    class Config:
        from_attributes = True  # allows conversion from ORM objects


# --- Dependency to get a DB session ---


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- FastAPI setup ---

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# --- Routes ---


@app.post("/books/", response_model=BookResponse)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    book = Book(**book_data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: str, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/books/", response_model=list[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
