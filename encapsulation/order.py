from dataclasses import dataclass, field
from enum import Enum


class PaymentStatus(Enum):
    CANCELLED = "cancelled"
    PENDING = "pending"
    PAID = "paid"


class PaymentStatusError(Exception):
    pass


@dataclass
class LineItem:
    name: str
    price: int
    quantity: int

    @property
    def total_price(self) -> int:
        return self.price * self.quantity


@dataclass
class Order:
    items: list[LineItem] = field(default_factory=list)
    _payment_status: PaymentStatus = PaymentStatus.PENDING

    def add_item(self, item: LineItem):
        self.items.append(item)

    def set_payment_status(self, status: PaymentStatus) -> None:
        if self._payment_status == PaymentStatus.PAID:
            raise PaymentStatusError(
                "You can't change the status of an already paid order."
            )
        self._payment_status = status

    @property
    def total_price(self) -> int:
        return sum(item.total_price for item in self.items)
