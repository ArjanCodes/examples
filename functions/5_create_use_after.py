import logging
from typing import Protocol


class StripePaymentHandler:
    def handle_payment(self, amount: int) -> None:
        logging.info(f"Charging ${amount/100:.2f} using Stripe")


PRICES = {
    "burger": 10_00,
    "fries": 5_00,
    "drink": 2_00,
    "salad": 15_00,
}


class PaymentHandler(Protocol):
    def handle_payment(self, amount: int) -> None:
        ...


def order_food(items: list[str], payment_handler: PaymentHandler) -> None:
    total = sum(PRICES[item] for item in items)
    logging.info(f"Order total is ${total/100:.2f}.")
    payment_handler.handle_payment(total)
    logging.info("Order completed.")


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    order_food(["burger", "salad", "drink"], StripePaymentHandler())


if __name__ == "__main__":
    main()
