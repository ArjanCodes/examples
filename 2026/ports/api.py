from adapters.sqlalchemy_inventory import SqlAlchemyInventoryAdapter
from db import get_db
from domain.errors import InvalidQuantity, OutOfStock, UnknownSku
from domain.models import OrderRequest
from domain.use_cases import place_order
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.engine import Connection

router = APIRouter()


class PlaceOrderIn(BaseModel):
    sku: str
    qty: int = Field(..., gt=0)


class PlaceOrderOut(BaseModel):
    sku: str
    qty: int
    remaining_stock: int


@router.post("/orders", response_model=PlaceOrderOut)
def place_order_endpoint(
    payload: PlaceOrderIn,
    connection: Connection = Depends(get_db),
) -> PlaceOrderOut:
    try:
        result = place_order(
            OrderRequest(**payload.model_dump()),
            SqlAlchemyInventoryAdapter(conn=connection),
        )
    except InvalidQuantity as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except UnknownSku as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except OutOfStock as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

    return PlaceOrderOut(
        sku=result.sku,
        qty=result.qty,
        remaining_stock=result.remaining_stock,
    )
