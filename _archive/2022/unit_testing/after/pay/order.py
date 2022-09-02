from dataclasses import dataclass, field
from enum import Enum


class OrderStatus(Enum):
    OPEN = "open"
    PAID = "paid"


@dataclass
class LineItem:
    name: str
    price: int
    quantity: int = 1

    @property
    def total(self) -> int:
        return self.price * self.quantity


@dataclass
class Order:
    line_items: list[LineItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.OPEN

    @property
    def total(self) -> int:
        return sum(item.total for item in self.line_items)

    def pay(self) -> None:
        self.status = OrderStatus.PAID
