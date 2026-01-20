from dataclasses import dataclass

type UserId = int
type Sku = str


@dataclass(frozen=True)
class OrderRequest:
    user_id: UserId
    sku: Sku
    qty: int


@dataclass(frozen=True)
class OrderPlaced:
    sku: Sku
    qty: int
    remaining_stock: int
