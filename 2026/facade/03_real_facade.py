"""The facade turns a multi-step Stripe workflow into one domain operation."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol

from stripe import PaymentIntent, Stripe, StripeCardError, StripeCustomer


@dataclass(frozen=True)
class Order:
    id: str
    customer_email: str
    customer_name: str
    total_in_cents: int


class PaymentStatus(Enum):
    COMPLETED = auto()
    REQUIRES_CUSTOMER_ACTION = auto()
    DECLINED = auto()


@dataclass(frozen=True)
class PaymentResult:
    status: PaymentStatus
    payment_id: str | None = None
    action_token: str | None = None
    reason: str | None = None


class Payments(Protocol):
    """The one payment operation the application needs."""

    def pay(self, order: Order, payment_method: str) -> PaymentResult: ...


class StripeGateway(Protocol):
    def find_customer_by_email(self, email: str) -> StripeCustomer | None: ...

    def create_customer(
        self, email: str, name: str, metadata: dict[str, str]
    ) -> StripeCustomer: ...

    def create_payment_intent(
        self,
        amount: int,
        currency: str,
        payment_method: str,
        customer_id: str,
        metadata: dict[str, str],
    ) -> PaymentIntent: ...

    def confirm_payment_intent(
        self, payment_intent_id: str, payment_method: str
    ) -> PaymentIntent: ...


class PaymentService:
    """Hides Stripe's customer, intent, confirmation, and error-handling workflow."""

    def __init__(self, stripe: StripeGateway) -> None:
        self._stripe = stripe

    def pay(self, order: Order, payment_method: str) -> PaymentResult:
        try:
            customer = self._find_or_create_customer(order)
            intent = self._stripe.create_payment_intent(
                amount=order.total_in_cents,
                currency="eur",
                payment_method=payment_method,
                customer_id=customer.id,
                metadata={"order_id": order.id, "customer_email": order.customer_email},
            )
            confirmed_intent = self._stripe.confirm_payment_intent(
                intent.id, payment_method
            )
        except StripeCardError as error:
            return PaymentResult(PaymentStatus.DECLINED, reason=str(error))

        return self._to_payment_result(confirmed_intent)

    def _find_or_create_customer(self, order: Order) -> StripeCustomer:
        customer = self._stripe.find_customer_by_email(order.customer_email)
        if customer is not None:
            return customer
        return self._stripe.create_customer(
            email=order.customer_email,
            name=order.customer_name,
            metadata={"first_order_id": order.id},
        )

    @staticmethod
    def _to_payment_result(intent: PaymentIntent) -> PaymentResult:
        if intent.status == "succeeded":
            return PaymentResult(PaymentStatus.COMPLETED, payment_id=intent.id)
        if intent.status == "requires_action":
            return PaymentResult(
                PaymentStatus.REQUIRES_CUSTOMER_ACTION,
                payment_id=intent.id,
                action_token=intent.client_secret,
            )
        return PaymentResult(
            PaymentStatus.DECLINED, reason="The payment could not be completed."
        )


def pay_for_order(payments: Payments, order: Order, payment_method: str) -> str:
    result = payments.pay(order, payment_method)
    if result.status is PaymentStatus.COMPLETED:
        return f"payment complete: {result.payment_id}"
    if result.status is PaymentStatus.REQUIRES_CUSTOMER_ACTION:
        return f"customer action required: {result.action_token}"
    return f"payment declined: {result.reason}"


def main() -> None:
    order = Order("order-42", "ada@example.com", "Ada Lovelace", 2_500)
    print(pay_for_order(PaymentService(Stripe()), order, "pm_card_visa"))

    # action required
    order = Order("order-43", "ada@example.com", "Ada Lovelace", 2_500)
    print(pay_for_order(PaymentService(Stripe()), order, "pm_card_authentication"))

    # card declined
    order = Order("order-44", "ada@example.com", "Ada Lovelace", 2_500)
    print(pay_for_order(PaymentService(Stripe()), order, "pm_card_declined"))
