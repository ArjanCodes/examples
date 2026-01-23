from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from ..domain.errors import InvalidQuantity, OutOfStock, UnknownSku
from ..domain.models import OrderRequest, Sku
from ..domain.ports import InventoryPort
from ..domain.use_cases import place_order

router = APIRouter()


class PlaceOrderIn(BaseModel):
    sku: str
    qty: int = Field(..., gt=0)


class PlaceOrderOut(BaseModel):
    sku: str
    qty: int
    remaining_stock: int


def get_inventory() -> InventoryPort:
    """
    Stub for FastAPI DI. The real provider is wired in main.py.
    """
    raise NotImplementedError


@router.post("/orders", response_model=PlaceOrderOut)
def place_order_endpoint(
    payload: PlaceOrderIn,
    inventory: InventoryPort = Depends(get_inventory),
) -> PlaceOrderOut:
    try:
        result = place_order(
            OrderRequest(sku=Sku(payload.sku), qty=payload.qty),
            inventory,
        )
    except InvalidQuantity as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except UnknownSku as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except OutOfStock as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

    return PlaceOrderOut(
        sku=str(result.sku),
        qty=result.qty,
        remaining_stock=result.remaining_stock,
    )
