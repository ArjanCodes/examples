from typing import Any

from db import get_db
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.engine import Connection

router = APIRouter()


class PlaceOrderIn(BaseModel):
    sku: str
    qty: int = Field(..., gt=0)


class PlaceOrderOut(BaseModel):
    sku: str
    qty: int
    remaining_stock: int


def place_order(db: Connection, sku: str, qty: int) -> dict[str, Any]:
    """
    😬 MIXED: domain rules + DB access + HTTP errors + response shaping.
    """
    if qty <= 0:
        raise HTTPException(status_code=400, detail="qty must be > 0")

    row = db.execute(
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
    db.execute(
        text("UPDATE inventory SET stock = stock - :qty WHERE sku=:sku"),
        {"sku": sku, "qty": qty},
    )
    remaining = db.execute(
        text("SELECT stock FROM inventory WHERE sku=:sku"),
        {"sku": sku},
    ).scalar_one()

    # API response shaping in the domain-y function
    return {"status": "ok", "sku": sku, "qty": qty, "remaining_stock": int(remaining)}


@router.post("/orders", response_model=PlaceOrderOut)
def place_order_endpoint(
    payload: PlaceOrderIn,
    connection: Connection = Depends(get_db),
) -> PlaceOrderOut:
    result = place_order(connection, payload.sku, payload.qty)
    return PlaceOrderOut(**result)
