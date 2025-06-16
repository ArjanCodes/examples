import secrets

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, dataclasses

app = FastAPI()

# --- DOMAIN MODEL (Pydantic Dataclass) ---


def generate_id() -> str:
    return secrets.token_hex(12)


@dataclasses.dataclass
class Book:
    title: str
    author: str
    pages: int = 0
    id: str = dataclasses.Field(default_factory=generate_id)


# --- API MODELS (Pydantic BaseModels) ---


class BookCreate(BaseModel):
    title: str
    author: str
    pages: int = 0

    class Config:
        from_attributes = True


class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    pages: int

    class Config:
        from_attributes = True


# --- FAKE IN-MEMORY DB ---

books_db: dict[str, Book] = {}

# --- ROUTES ---


@app.post("/books/", response_model=BookResponse)
def create_book(book_data: BookCreate):
    book = Book(**book_data.model_dump())
    books_db[book.id] = book
    return BookResponse.model_validate(book)


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: str):
    book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.model_validate(book)


@app.get("/books/", response_model=list[BookResponse])
def list_books():
    return [BookResponse.model_validate(book) for book in books_db.values()]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
