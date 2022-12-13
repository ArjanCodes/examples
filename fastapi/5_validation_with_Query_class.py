from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int


items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0),
    1: Item(name="Pliers", price=5.99, count=20, id=1),
    2: Item(name="Nails", price=1.99, count=100, id=2),
}


@app.get("/")
def index():
    return {"items": items}


@app.get("/items/{item_id}")
def query_item_by_id(item_id: int):
    if item_id not in items:
        HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")

    return items[item_id]


@app.get("/items/")
def query_item_by_parameters(
    name: str | None = None, price: float | None = None, count: int | None = None
):
    def check_item(item: Item):
        if name is not None and item.name != name:
            return False
        if price is not None and item.price != price:
            return False
        if count is not None and item.count != count:
            return False
        return True

    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "price": price, "count": count},
        "selection": selection,
    }


@app.post("/")
def add_item(item: Item):
    if item.id in items:
        HTTPException(status_code=400, detail=f"Item with {item.id=} already exists.")

    items[item.id] = item
    return {"added": item}


# We can place further restrictions on allowed arguments by using the Query class.
# In this case we are setting a lower bound for valid values.
@app.put("/update/{item_id}")
def update(
    item_id: int,
    name: str | None = None,
    price: float | None = Query(default=None, gt=0.0),
    count: int | None = Query(default=None, ge=0),
):
    if all(info is None for info in (name, price, count)):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update."
        )

    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count

    return {"updated": item}


@app.delete("/delete/{item_id}")
def delete_item(item_id: int):

    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} does not exist."
        )

    item = items.pop(item_id)
    return {"deleted": item}
