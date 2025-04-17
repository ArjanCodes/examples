from enum import StrEnum
from typing import Callable


class PaymentMethod(StrEnum):
    PAYPAL = "paypal"
    CARD = "card"


type PaymentFn = Callable[[int], None]


def pay_paypal(amount: int) -> None:
    print(f"Paying {amount} using Paypal")


def pay_stripe(amount: int) -> None:
    print(f"Paying {amount} using Stripe")


def get_payment_method(payment_type: str) -> PaymentFn:
    if payment_type == PaymentMethod.PAYPAL:
        return pay_paypal
    elif payment_type == PaymentMethod.CARD:
        return pay_stripe
    else:
        raise ValueError(f"Unsupported payment type: {payment_type}")


PAYMENT_METHODS: dict[PaymentMethod, PaymentFn] = {
    PaymentMethod.CARD: pay_stripe,
    PaymentMethod.PAYPAL: pay_paypal,
}


def main():
    # using the dictionary
    my_payment_fn = PAYMENT_METHODS[PaymentMethod.PAYPAL]
    my_payment_fn(100)

    # using the function
    my_payment_fn = get_payment_method("card")
    my_payment_fn(100)


if __name__ == "__main__":
    main()
