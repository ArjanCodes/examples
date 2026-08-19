from dataclasses import dataclass


class StripeCardError(Exception):
    pass


@dataclass
class StripeCustomer:
    id: str
    email: str
    name: str


@dataclass
class PaymentIntent:
    id: str
    status: str
    client_secret: str


class Stripe:
    """A tiny, deterministic stand-in for the Stripe SDK."""

    def __init__(self) -> None:
        self._customers_by_email: dict[str, StripeCustomer] = {}
        self._payment_intents: dict[str, PaymentIntent] = {}

    def find_customer_by_email(self, email: str) -> StripeCustomer | None:
        return self._customers_by_email.get(email)

    def create_customer(
        self, email: str, name: str, metadata: dict[str, str]
    ) -> StripeCustomer:
        customer = StripeCustomer(
            id=f"cus_{len(self._customers_by_email) + 1:03}",
            email=email,
            name=name,
        )
        self._customers_by_email[email] = customer
        return customer

    def create_payment_intent(
        self,
        amount: int,
        currency: str,
        payment_method: str,
        customer_id: str,
        metadata: dict[str, str],
    ) -> PaymentIntent:
        if payment_method == "pm_card_declined":
            raise StripeCardError("Your card was declined.")
        payment_intent = PaymentIntent(
            id=f"pi_{len(self._payment_intents) + 1:03}",
            status="requires_confirmation",
            client_secret=f"pi_{len(self._payment_intents) + 1:03}_secret",
        )
        self._payment_intents[payment_intent.id] = payment_intent
        return payment_intent

    def confirm_payment_intent(
        self, payment_intent_id: str, payment_method: str
    ) -> PaymentIntent:
        intent = self._payment_intents[payment_intent_id]
        intent.status = (
            "requires_action"
            if payment_method == "pm_card_authentication"
            else "succeeded"
        )
        return intent
