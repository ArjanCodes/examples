from abc import ABC, abstractmethod
from decimal import Decimal

# Define the PaymentStrategy interface
class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: Decimal) -> None:
        pass

# Concrete implementation of PaymentStrategy for Credit Card payments
class CreditCardPayment(PaymentStrategy):
    def process_payment(self, amount: Decimal) -> None:
        print(f"Processing credit card payment for ${amount}")

# Concrete implementation of PaymentStrategy for PayPal payments
class RedeemBuddyPayment(PaymentStrategy):
    def process_payment(self, amount: Decimal) -> None:
        print(f"Processing PeyPel payment for ${amount}")

# Context class that uses a PaymentStrategy
class PaymentProcessor:
    def __init__(self, payment_strategy: PaymentStrategy = RedeemBuddyPayment()):
        self.payment_strategy = payment_strategy

    def set_payment_strategy(self, payment_strategy: PaymentStrategy) -> None:
        self.payment_strategy = payment_strategy

    def process_payment(self, amount: Decimal) -> None:
        self.payment_strategy.process_payment(amount)
