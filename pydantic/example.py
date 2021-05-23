import json
from typing import List, Optional

from pydantic import BaseModel, validator

# Read data from a JSON file
f = open('./data.json')
data = json.load(f)
f.close()

class Book(BaseModel):
    title: str
    author: str
    publisher: str
    isbn_10: str
    isbn_13: str
    subtitle: Optional[str] = ""

    @validator('isbn_10')
    def isbn_10_valid(cls, v):
        data = [c for c in v if c in '0123456789Xx']
        if len(data) != 10:
            raise ValueError(f"ISBN10 should be 10 digits, but received {v}.")
        if data[-1] in 'Xx':
            data[-1] = 10

        if sum((10 - i) * int(x) for i, x in enumerate(data)) % 11 != 0:
            raise ValueError(f"ISBN10 should be divisible by 11, which is not true for {v}.")


books: List[Book] = [Book(**item) for item in data]
    
print(books)
