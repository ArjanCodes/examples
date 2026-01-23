from dataclasses import dataclass


@dataclass(frozen=True)
class OrderRequest:
    sku: str
    qty: int


@dataclass(frozen=True)
class OrderPlaced:
    sku: str
    qty: int
    remaining_stock: int
