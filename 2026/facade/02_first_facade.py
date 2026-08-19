"""Version 2: the workflow is hidden, but Stripe concepts still leak out."""

from dataclasses import dataclass

from stripe import PaymentIntent, Stripe, StripeCardError


@dataclass(frozen=True)
class Order:
    id: str
    customer_email: str
    customer_name: str
    total_in_cents: int


class PaymentService:
    """A convenient wrapper around Stripe's multi-step checkout workflow."""

    def __init__(self, stripe: Stripe) -> None:
        self._stripe = stripe

    def pay(self, order: Order, payment_method: str) -> PaymentIntent:
        customer = self._stripe.find_customer_by_email(order.customer_email)
        if customer is None:
            customer = self._stripe.create_customer(
                email=order.customer_email,
                name=order.customer_name,
                metadata={"first_order_id": order.id},
            )
        intent = self._stripe.create_payment_intent(
            amount=order.total_in_cents,
            currency="eur",
            payment_method=payment_method,
            customer_id=customer.id,
            metadata={"order_id": order.id, "customer_email": order.customer_email},
        )
        return self._stripe.confirm_payment_intent(intent.id, payment_method)


def pay_for_order(payments: PaymentService, order: Order, payment_method: str) -> str:
    try:
        intent = payments.pay(order, payment_method)
    except StripeCardError:  # Stripe's exception still leaks into application code.
        return "payment declined"

    if intent.status == "requires_action":  # And so do Stripe status strings.
        return f"customer action required: {intent.client_secret}"
    if intent.status == "succeeded":
        return f"payment complete: {intent.id}"
    return f"unexpected Stripe status: {intent.status}"


def main() -> None:
    order = Order("order-42", "ada@example.com", "Ada Lovelace", 2_500)
    print(pay_for_order(PaymentService(Stripe()), order, "pm_card_visa"))

    # action required
    order = Order("order-43", "ada@example.com", "Ada Lovelace", 2_500)
    print(pay_for_order(PaymentService(Stripe()), order, "pm_card_authentication"))

    # card declined
    order = Order("order-44", "ada@example.com", "Ada Lovelace", 2_500)
    print(pay_for_order(PaymentService(Stripe()), order, "pm_card_declined"))


if __name__ == "__main__":
    main()
