import random
import string

from pos.order import Order, OrderStatus
from pos.payment import StripePaymentProcessor


def generate_id(length: int = 6) -> str:
    """Helper function for generating an id."""
    return "".join(random.choices(string.ascii_uppercase, k=length))


class POSSystem:
    def __init__(self):
        self.payment_processor = StripePaymentProcessor(self)
        self.orders: dict[str, Order] = {}

    def setup_payment_processor(self) -> None:
        self.payment_processor.connect_to_service()

    def register_order(self, order: Order) -> str:
        order_id = generate_id()
        self.orders[order_id] = order
        return order_id

    def find_order(self, order_id: str) -> Order:
        return self.orders[order_id]

    def compute_order_total_price(self, order: Order) -> int:
        total = 0
        for i in range(len(order.prices)):
            total += order.quantities[i] * order.prices[i]
        return total

    def process_order(self, order_id: str):
        order = self.find_order(order_id)
        self.payment_processor.process_payment(order)
        order.status = OrderStatus.PAID
        print("Shipping order to customer.")
