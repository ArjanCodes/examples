from pydantic import BaseModel, ValidationError, validator
from pydantic.dataclasses import dataclass


@dataclass
class Book:
    title: str
    pages: int

    @validator("pages")
    def pages_must_be_positive(cls, v: int):
        if v < 0:
            raise ValueError("Pages must be a positive integer")
        return v


class Author(BaseModel):
    name: str
    age: int

    @validator("age")
    def age_must_be_positive(cls, v: int):
        if v < 0:
            raise ValueError("Age must be a positive integer")
        return v


def main() -> None:
    # Valid input
    book = Book(title="1984", pages=328)  # pages will be converted to int

    # print(book.model_dump())  # {'title': '1984', 'pages': 328}

    # Invalid input – will raise a ValidationError
    try:
        bad_book = Book(title="The Hobbit", pages="three hundred")
    except ValidationError as e:
        print(e)

    author = Author(name="J.R.R. Tolkien", age=81)
    print(author.model_dump())  # {'name': 'J.R.R. Tolkien', 'age': 81}


if __name__ == "__main__":
    main()
