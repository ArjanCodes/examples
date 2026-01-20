from __future__ import annotations

from fastapi import FastAPI

from .adapters import api
from .db import init_db
from .wiring import get_inventory_port

app = FastAPI(title="AFTER - ports & adapters")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


# Wire the dependency: the API asks for InventoryPort, we provide it via SQLAlchemy adapter.
app.dependency_overrides[api.get_inventory] = get_inventory_port

app.include_router(api.router)
