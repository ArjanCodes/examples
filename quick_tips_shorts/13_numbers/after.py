from typing import Protocol


class PaymentHandler(Protocol):
    def handle_payment(self, amount: int) -> None:
        ...


class StripePaymentHandler:
    def handle_payment(self, amount: int) -> None:
        print(f"Charging ${amount/100:.2f} using Stripe")


PRICES = {
    "burger": 10_00,
    "fries": 5_00,
    "drink": 2_00,
    "salad": 15_00,
    "tesla": 60_000_00,
}


def order_food(items: list[str], payment_handler: PaymentHandler) -> None:
    total = sum(PRICES[item] for item in items)
    print(f"Your order is ${total/100:.2f}.")
    payment_handler.handle_payment(total)
    print("Thanks for your business!")


def main() -> None:
    order_food(["burger", "salad", "drink"], StripePaymentHandler())


if __name__ == "__main__":
    main()
