from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Category(Enum):
    TOOLS = 'tools'
    CONSUMABLES = 'consumables'


class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category


items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES),
}


@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}


# Path parameters can be specified with {} directly in the path (similar to f-string syntax)
# These parameters will be forwarded to the decorated function as keyword arguments.
@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")

    return items[item_id]


# Function parameters that are not path parameters can be specified as query parameters in the URL
# Here we can query items like this /items?count=20
Selection = dict[str, str | int | float | Category]  # dictionary containing the user's query arguments
@app.get("/items/")
def query_item_by_parameters(
        name: str | None = None, price: float | None = None, count: int | None = None, category: Category | None = None
) -> dict[str,  Selection | list[Item]]:
    def check_item(item: Item):
        """Check if the item matches the query arguments from the outer scope."""
        if name is not None and item.name != name:
            return False
        if price is not None and item.price != price:
            return False
        if count is not None and item.count != count:
            return False
        if category is not None and item.category is not category:
            return False
        return True

    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection,
    }
