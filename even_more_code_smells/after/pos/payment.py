class PaymentServiceConnectionError(Exception):
    """Custom error that is raised when we couldn't connect to the payment service."""


class StripePaymentProcessor:
    def __init__(self):
        self.connected = False

    def connect_to_service(self):
        print("Connecting to payment processing service...done!")
        self.connected = True

    def process_payment(self, reference: str, price: int):
        if not self.connected:
            raise PaymentServiceConnectionError()
        print(f"Processing payment of ${(price / 100):.2f}, reference: {reference}.")
