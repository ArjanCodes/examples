from typing import Protocol

from .models import Sku


class InventoryPort(Protocol):
    def get_stock(self, sku: Sku) -> int: ...
    def reserve(self, sku: Sku, qty: int) -> int: ...
