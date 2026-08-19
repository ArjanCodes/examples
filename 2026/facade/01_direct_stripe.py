"""Version 1: application code performs Stripe's workflow itself."""

from dataclasses import dataclass

from stripe import Stripe, StripeCardError


@dataclass(frozen=True)
class Order:
    id: str
    customer_email: str
    customer_name: str
    total_in_cents: int


def pay_for_order(stripe: Stripe, order: Order, payment_method: str) -> str:
    """The application now has to understand every Stripe step and type."""
    customer = stripe.find_customer_by_email(order.customer_email)
    if customer is None:
        customer = stripe.create_customer(
            email=order.customer_email,
            name=order.customer_name,
            metadata={"first_order_id": order.id},
        )

    try:
        intent = stripe.create_payment_intent(
            amount=order.total_in_cents,
            currency="eur",
            payment_method=payment_method,
            customer_id=customer.id,
            metadata={"order_id": order.id, "customer_email": order.customer_email},
        )
        confirmed_intent = stripe.confirm_payment_intent(intent.id, payment_method)
    except StripeCardError:
        return "payment declined"

    if confirmed_intent.status == "requires_action":
        return f"customer action required: {confirmed_intent.client_secret}"
    if confirmed_intent.status == "succeeded":
        return f"payment complete: {confirmed_intent.id}"
    return f"unexpected Stripe status: {confirmed_intent.status}"


def main() -> None:
    order = Order("order-42", "ada@example.com", "Ada Lovelace", 2_500)
    print(pay_for_order(Stripe(), order, "pm_card_visa"))

    # action required
    order = Order("order-43", "ada@example.com", "Ada Lovelace", 2_500)
    print(pay_for_order(Stripe(), order, "pm_card_authentication"))

    # card declined
    order = Order("order-44", "ada@example.com", "Ada Lovelace", 2_500)
    print(pay_for_order(Stripe(), order, "pm_card_declined"))


if __name__ == "__main__":
    main()
