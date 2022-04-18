import os

from dotenv import load_dotenv

from pay.order import LineItem, Order
from pay.payment import pay_order
from pay.processor import PaymentProcessor


def main():
    load_dotenv()
    api_key = os.getenv("API_KEY") or ""
    payment_processor = PaymentProcessor(api_key)
    # Test card number: 1249190007575069
    order = Order()
    order.line_items.append(LineItem(name="Shoes", price=100_00, quantity=2))
    order.line_items.append(LineItem(name="Hat", price=50_00))
    pay_order(order, payment_processor)


if __name__ == "__main__":
    main()
