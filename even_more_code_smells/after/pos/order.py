import functools
from dataclasses import dataclass, field
from enum import Enum, auto

from pos.customer import Customer


class OrderStatus(Enum):
    """Order status"""

    OPEN = auto()
    PAID = auto()
    CANCELLED = auto()
    DELIVERED = auto()
    RETURNED = auto()


@dataclass
class LineItem:
    item: str
    quantity: int
    price: int

    @property
    def total_price(self) -> int:
        return self.quantity * self.price


@dataclass
class Order:
    customer: Customer
    items: list[LineItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.OPEN

    def add_line_item(self, item: LineItem) -> None:
        self.items.append(item)

    @property
    def total_price(self) -> int:
        return functools.reduce(lambda x, y: x + y.total_price, self.items, 0)
        # or using a for loop:
        # total = 0
        # for item in self.items:
        #     total += item.total_price
        # return total
