from typing import Protocol

from pay.order import Order


class PaymentProcessor(Protocol):
    def charge(self, card: str, month: int, year: int, amount: int) -> None:
        """Charge the card."""


def pay_order(order: Order, payment_processor: PaymentProcessor):
    if order.total == 0:
        raise ValueError("Can't pay an order with total 0.")
    card = input("Please enter your card number: ")
    month = int(input("Please enter the card expiry month: "))
    year = int(input("Please enter the card expiry year: "))
    payment_processor.charge(card, month, year, amount=order.total)
    order.pay()
