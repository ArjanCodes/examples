from api import get_inventory, router
from fastapi import FastAPI

from .adapters.sqlalchemy_inventory import SqlAlchemyInventoryAdapter
from .db import engine, init_db

app = FastAPI(title="Ports & adapters")


def get_inventory_port():
    conn = engine.connect()
    try:
        yield SqlAlchemyInventoryAdapter(conn)
    finally:
        conn.close()


@app.on_event("startup")
def on_startup() -> None:
    init_db("sqlite:///./after.db")


# Wire the dependency
app.dependency_overrides[get_inventory] = get_inventory_port

app.include_router(router)
