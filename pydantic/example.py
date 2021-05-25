"""
Basic example showing how to read and validate data from a file using Pydantic.
"""

import json
from typing import List, Optional

import pydantic


class Book(pydantic.BaseModel):
    """Represents a book with that you can read from a JSON file"""

    title: str
    author: str
    publisher: str
    price: float
    isbn_10: Optional[str] = ""
    isbn_13: Optional[str] = ""
    subtitle: Optional[str] = ""

    @pydantic.root_validator(pre=True)
    @classmethod
    def check_isbn_10_or_13(cls, values):
        """Make sure there is either an isbn_10 or isbn_13 value defined"""
        assert "isbn_10" in values or "isbn_13" in values
        return values

    @pydantic.validator("isbn_10")
    @classmethod
    def isbn_10_valid(cls, value):
        """Validator to check whether ISBN10 is valid"""
        chars = [c for c in value if c in "0123456789Xx"]
        if len(chars) != 10:
            raise ValueError(f"ISBN10 should be 10 digits, but received {value}.")
        if chars[-1] in "Xx":
            chars[-1] = 10

        if sum((10 - i) * int(x) for i, x in enumerate(chars)) % 11 != 0:
            raise ValueError(f"ISBN10 digit sum should be divisible by 11: {value}.")

    class Config:
        """Pydantic config class"""

        allow_mutation = False
        anystr_lower = True


# Read data from a JSON file
with open("./data.json") as file:
    data = json.load(file)
    books: List[Book] = [Book(**item) for item in data]
    print(books)
    print(books[0].dict(exclude={"price"}))
    print(books[1].copy())
