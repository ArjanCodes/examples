class Payment:
    def __new__(cls, payment_type: str):
        if payment_type == "paypal":
            return object.__new__(PaypalPayment)
        elif payment_type == "card":
            return object.__new__(StripePayment)

    def pay(self, amount: int) -> None:
        raise NotImplementedError


class PaypalPayment(Payment):
    def pay(self, amount: int) -> None:
        print(f"Paying ${amount / 100:.2f} using Paypal")


class StripePayment(Payment):
    def pay(self, amount: int) -> None:
        print(f"Paying ${amount / 100:.2f} using Stripe")


def main() -> None:
    my_payment = Payment("card")
    my_payment.pay(100)


if __name__ == "__main__":
    main()
