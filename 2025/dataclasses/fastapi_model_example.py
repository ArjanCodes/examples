import secrets
from dataclasses import dataclass, field

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# --- DOMAIN MODEL ---


def generate_id() -> str:
    return secrets.token_hex(12)


@dataclass
class Book:
    title: str
    author: str
    pages: int = 0
    id: str = field(default_factory=generate_id)


# --- Pydantic MODELS for API ---


class BookCreate(BaseModel):
    title: str
    author: str
    pages: int = 0


class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    pages: int


# --- FAKE DB ---

books_db: dict[str, Book] = {}


# --- ROUTES ---


@app.post("/books/", response_model=BookResponse)
def create_book(book_data: BookCreate):
    book = Book(**book_data.dict())  # ID is generated automatically
    books_db[book.id] = book
    return BookResponse(**book.__dict__)


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: str):
    book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse(**book.__dict__)


@app.get("/books/", response_model=list[BookResponse])
def list_books():
    return [BookResponse(**book.__dict__) for book in books_db.values()]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
