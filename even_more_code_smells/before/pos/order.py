from dataclasses import dataclass, field
from enum import Enum, auto


class OrderStatus(Enum):
    """Order status"""

    OPEN = auto()
    PAID = auto()
    CANCELLED = auto()
    DELIVERED = auto()
    RETURNED = auto()


@dataclass
class Order:
    customer_id: int = 0
    customer_name: str = ""
    customer_address: str = ""
    customer_postal_code: str = ""
    customer_city: str = ""
    customer_email: str = ""
    items: list[str] = field(default_factory=list)
    quantities: list[int] = field(default_factory=list)
    prices: list[int] = field(default_factory=list)
    status: OrderStatus = OrderStatus.OPEN

    def create_line_item(self, name: str, quantity: int, price: int) -> None:
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def pay(self, payment_type: str, security_code: str) -> None:
        if payment_type == "debit":
            print("Processing debit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = OrderStatus.PAID
        elif payment_type == "credit":
            print("Processing credit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = OrderStatus.PAID
        else:
            raise ValueError(f"Unknown payment type: {payment_type}")
