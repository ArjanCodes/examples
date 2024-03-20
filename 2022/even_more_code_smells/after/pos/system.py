import random
import string
from typing import Protocol

from pos.order import Order, OrderStatus


def generate_id(length: int = 6) -> str:
    """Helper function for generating an id."""
    return "".join(random.choices(string.ascii_uppercase, k=length))


class PaymentProcessor(Protocol):
    def process_payment(self, reference: str, price: int) -> None: ...


class POSSystem:
    def __init__(self, payment_processor: PaymentProcessor):
        self.payment_processor = payment_processor
        self.orders: dict[str, Order] = {}

    def register_order(self, order: Order) -> None:
        order.id = generate_id()
        self.orders[order.id] = order

    def find_order(self, order_id: str) -> Order:
        return self.orders[order_id]

    def process_order(self, order: Order) -> None:
        self.payment_processor.process_payment(order.id, order.total_price)
        order.set_status(OrderStatus.PAID)
        print("Shipping order to customer.")
