from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

DB_URL = "sqlite:///./before.db"
engine: Engine = create_engine(DB_URL, future=True)

app = FastAPI(title="BEFORE - mixed concerns")


class PlaceOrderIn(BaseModel):
    user_id: int
    sku: str
    qty: int = Field(..., gt=0)


class PlaceOrderOut(BaseModel):
    status: str
    sku: str
    qty: int
    remaining_stock: int


def init_db() -> None:
    """Create table + seed data if needed."""
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS inventory (
                    sku TEXT PRIMARY KEY,
                    stock INTEGER NOT NULL
                )
                """
            )
        )
        # Seed only if empty
        count = conn.execute(text("SELECT COUNT(*) FROM inventory")).scalar_one()
        if count == 0:
            conn.execute(
                text("INSERT INTO inventory(sku, stock) VALUES (:sku, :stock)"),
                [{"sku": "ABC", "stock": 10}, {"sku": "XYZ", "stock": 2}],
            )


@app.on_event("startup")
def on_startup() -> None:
    init_db()


def place_order(db_engine: Engine, user_id: int, sku: str, qty: int) -> dict[str, Any]:
    """
    😬 MIXED: domain rules + DB access + HTTP errors + response shaping.
    """
    if qty <= 0:
        raise HTTPException(status_code=400, detail="qty must be > 0")

    with db_engine.begin() as conn:
        row = conn.execute(
            text("SELECT stock FROM inventory WHERE sku=:sku"),
            {"sku": sku},
        ).fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="unknown sku")

        available = int(row.stock)
        if available < qty:
            raise HTTPException(
                status_code=409,
                detail=f"out of stock: requested {qty}, available {available}",
            )

        # Not fully atomic in a concurrent setting, but ok for demo
        conn.execute(
            text("UPDATE inventory SET stock = stock - :qty WHERE sku=:sku"),
            {"sku": sku, "qty": qty},
        )
        remaining = conn.execute(
            text("SELECT stock FROM inventory WHERE sku=:sku"),
            {"sku": sku},
        ).scalar_one()

    # API response shaping in the domain-y function
    return {"status": "ok", "sku": sku, "qty": qty, "remaining_stock": int(remaining)}


@app.post("/orders", response_model=PlaceOrderOut)
def place_order_endpoint(payload: PlaceOrderIn) -> PlaceOrderOut:
    result = place_order(engine, payload.user_id, payload.sku, payload.qty)
    return PlaceOrderOut(**result)
