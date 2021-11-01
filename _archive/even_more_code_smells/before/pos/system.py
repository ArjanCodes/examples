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

    def setup_payment_processor(self, url: str) -> None:
        self.payment_processor.connect_to_service(url)

    def register_order(self, order: Order):
        order.id = generate_id()
        self.orders[order.id] = order

    def find_order(self, order_id: str) -> Order:
        return self.orders[order_id]

    def compute_order_total_price(self, order: Order) -> int:
        total = 0
        for i in range(len(order.prices)):
            total += order.quantities[i] * order.prices[i]
        return total

    def process_order(self, order: Order) -> None:
        self.payment_processor.process_payment(order.id)
        order.set_status(OrderStatus.PAID)
        print("Shipping order to customer.")
