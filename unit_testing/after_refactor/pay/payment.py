from pay.order import Order
from pay.processor import PaymentProcessor


def pay_order(order: Order, payment_processor: PaymentProcessor):
    card = input("Please enter your card number: ")
    month = int(input("Please enter the card expiry month: "))
    year = int(input("Please enter the card expiry year: "))
    payment_processor.charge(card, month, year, amount=order.total)
