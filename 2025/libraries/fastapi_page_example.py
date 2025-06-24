import uvicorn
from fastapi import FastAPI
from fastapi_pagination import Page, add_pagination, paginate
from pydantic import BaseModel

app = FastAPI()


# --- Define your Pydantic model ---
class Item(BaseModel):
    id: int
    name: str


# --- Fake database ---
items_db: list[Item] = [
    Item(id=i, name=f"Item {i}") for i in range(1, 101)
]  # 100 items


# --- Paginated endpoint ---
@app.get("/items", response_model=Page[Item])
def get_items():
    return paginate(items_db)


# --- Activate pagination ---
add_pagination(app)


def main() -> None:
    uvicorn.run("fastapi_page_example:app", host="127.0.0.1", port=8000, reload=True)


# --- Run server directly ---
if __name__ == "__main__":
    main()
