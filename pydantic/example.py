import json
from typing import List, Optional

import pydantic

# Read data from a JSON file
f = open("./data.json")
data = json.load(f)
f.close()


class Book(pydantic.BaseModel):
    """Represents a book with that you can read from a JSON file"""

    title: str
    author: str
    publisher: str
    isbn_10: str
    isbn_13: str
    subtitle: Optional[str] = ""

    @pydantic.validator("isbn_10")
    def isbn_10_valid(cls, value):
        chars = [c for c in value if c in "0123456789Xx"]
        if len(chars) != 10:
            raise ValueError(f"ISBN10 should be 10 digits, but received {value}.")
        if chars[-1] in "Xx":
            chars[-1] = 10

        if sum((10 - i) * int(x) for i, x in enumerate(chars)) % 11 != 0:
            raise ValueError(f"ISBN10 should be divisible by 11, which is not true for {value}.")


books: List[Book] = [Book(**item) for item in data]

print(books)
