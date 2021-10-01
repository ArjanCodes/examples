from typing import Protocol

from pos.order import Order


class PaymentServiceConnectionError(Exception):
    """Custom error that is raised when we couldn't connect to the payment service."""


class OrderRepository(Protocol):
    def find_order(self, order_id: str) -> Order:
        raise NotImplementedError()

    def compute_order_total_price(self, order: Order) -> int:
        raise NotImplementedError()


class StripePaymentProcessor:
    def __init__(self, system: OrderRepository):
        self.connected = False
        self.system = system

    def connect_to_service(self):
        print("Connecting to payment processing service...done!")
        self.connected = True

    def process_payment(self, order_id: str, order: Order):
        if not self.connected:
            raise PaymentServiceConnectionError()
        total_price = self.system.compute_order_total_price(order)
        print(
            f"Processing payment of ${(total_price / 100):.2f}, reference: {order_id}."
        )
