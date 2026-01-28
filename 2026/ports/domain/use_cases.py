from .errors import InvalidQuantity, OutOfStock, UnknownSku
from .models import OrderPlaced, OrderRequest
from .ports import InventoryPort


def place_order(req: OrderRequest, inventory: InventoryPort) -> OrderPlaced:
    if req.qty <= 0:
        raise InvalidQuantity()

    if not inventory.exists_sku(req.sku):
        raise UnknownSku(req.sku)

    available = inventory.get_stock(req.sku)
    if available < req.qty:
        raise OutOfStock(req.sku, req.qty, available)

    remaining = inventory.reserve(req.sku, req.qty)
    return OrderPlaced(sku=req.sku, qty=req.qty, remaining_stock=remaining)
