from dataclasses import dataclass, field

from fastapi import FastAPI

app = FastAPI()


@dataclass
class Item:
    id: str
    name: str
    tags: list[str] = field(default_factory=list)
    description: str | None = None


@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int) -> Item:
    return Item(id=str(item_id), name="ArjanCodes")
