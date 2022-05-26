from enum import Enum
from typing import Protocol


class PaymentMethod(Enum):
    PAYPAL = "paypal"
    CARD = "card"


class Payment(Protocol):
    def pay(self, amount: int) -> None:
        ...


class PaypalPayment(Payment):
    def pay(self, amount: int) -> None:
        print(f"Paying {amount} using Paypal")


class StripePayment(Payment):
    def pay(self, amount: int) -> None:
        print(f"Paying {amount} using Stripe")


PAYMENT_METHODS: dict[PaymentMethod, type[Payment]] = {
    PaymentMethod.CARD: StripePayment,
    PaymentMethod.PAYPAL: PaypalPayment,
}


def main():
    my_payment = PAYMENT_METHODS[PaymentMethod.PAYPAL]()
    my_payment.pay(100)


if __name__ == "__main__":
    main()
