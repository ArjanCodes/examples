from .errors import InvalidQuantity, OutOfStock
from .models import OrderPlaced, OrderRequest
from .ports import InventoryPort


def place_order(req: OrderRequest, inventory: InventoryPort) -> OrderPlaced:
    # Domain rule: qty must be positive
    if req.qty <= 0:
        raise InvalidQuantity("qty must be > 0")

    available = inventory.get_stock(req.sku)
    if available < req.qty:
        raise OutOfStock(str(req.sku), req.qty, available)

    remaining = inventory.reserve(req.sku, req.qty)
    return OrderPlaced(sku=req.sku, qty=req.qty, remaining_stock=remaining)
