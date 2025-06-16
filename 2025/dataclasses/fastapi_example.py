import secrets

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    title: str
    author: str
    pages: int = 0


books_db: dict[str, Book] = {}


def generate_id() -> str:
    # Generate a 24-character hex string (like MongoDB ObjectID)
    return secrets.token_hex(12)


@app.post("/books/")
def create_book(book: Book):
    book_id = generate_id()
    books_db[book_id] = book
    return {"id": book_id, "book": book}


@app.get("/books/{book_id}")
def get_book(book_id: str):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": book_id, "book": books_db[book_id]}


@app.get("/books/")
def list_books():
    return [{"id": book_id, "book": book} for book_id, book in books_db.items()]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
