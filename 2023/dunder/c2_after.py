from enum import StrEnum, auto
from typing import Protocol


class PaymentMethod(StrEnum):
    PAYPAL = auto()
    CARD = auto()


class Payment(Protocol):
    def pay(self, amount: int) -> None: ...


class PaypalPayment:
    def pay(self, amount: int) -> None:
        print(f"Paying ${amount / 100:.2f} using Paypal")


class StripePayment:
    def pay(self, amount: int) -> None:
        print(f"Paying ${amount / 100:.2f} using Stripe")


def create_payment(method: PaymentMethod) -> Payment:
    if method == PaymentMethod.PAYPAL:
        return PaypalPayment()
    elif method == PaymentMethod.CARD:
        return StripePayment()
    else:
        raise NotImplementedError


def main():
    my_payment = create_payment(PaymentMethod.PAYPAL)
    my_payment.pay(10000)


if __name__ == "__main__":
    main()
