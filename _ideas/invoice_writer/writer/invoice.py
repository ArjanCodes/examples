from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LineItem:
    description: str
    quantity: int
    price: int
    vat_rate: float = 0.2

    def subtotal(self) -> int:
        return self.quantity * self.price

    def vat(self) -> int:
        return int(self.subtotal() * self.vat_rate)


@dataclass
class Customer:
    name: str
    address: str
    phone: str
    email: str


@dataclass
class Invoice:
    reference: str
    date: datetime
    customer: Customer
    items: list[LineItem] = field(default_factory=list)

    def add_item(self, item: LineItem):
        self.items.append(item)

    def total(self) -> int:
        return sum(item.subtotal() for item in self.items)

    def total_vat(self) -> int:
        return sum(item.vat() for item in self.items)
