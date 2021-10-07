from __future__ import annotations


class PaymentServiceConnectionError(Exception):
    """Custom error that is raised when we couldn't connect to the payment service."""


class StripePaymentProcessor:
    def __init__(self):
        self.connected = False

    @staticmethod
    def create(url: str) -> StripePaymentProcessor:
        obj = StripePaymentProcessor()
        obj.connect_to_service(url)
        return obj

    def connect_to_service(self, url: str) -> None:
        print(f"Connecting to payment processing service at url {url}... done!")
        self.connected = True

    def process_payment(self, reference: str, price: int) -> None:
        if not self.connected:
            raise PaymentServiceConnectionError()
        print(f"Processing payment of ${(price / 100):.2f}, reference: {reference}.")
