"""The facade is tested with a fake Stripe workflow, not the Stripe SDK."""

import importlib.util
import unittest
from pathlib import Path

from stripe import PaymentIntent, StripeCardError, StripeCustomer

module_path = Path(__file__).with_name("03_real_facade.py")
spec = importlib.util.spec_from_file_location("real_facade", module_path)
assert spec and spec.loader
real_facade = importlib.util.module_from_spec(spec)
spec.loader.exec_module(real_facade)

Order = real_facade.Order
PaymentResult = real_facade.PaymentResult
PaymentService = real_facade.PaymentService
PaymentStatus = real_facade.PaymentStatus
pay_for_order = real_facade.pay_for_order


class FakeStripe:
    def __init__(
        self,
        customer: StripeCustomer | None = None,
        confirmed_intent: PaymentIntent | None = None,
        create_error: Exception | None = None,
    ) -> None:
        self.customer = customer
        self.confirmed_intent = confirmed_intent or PaymentIntent(
            "pi_test", "succeeded", "secret"
        )
        self.create_error = create_error
        self.calls: list[tuple[str, object]] = []

    def find_customer_by_email(self, email: str) -> StripeCustomer | None:
        self.calls.append(("find_customer", email))
        return self.customer

    def create_customer(
        self, email: str, name: str, metadata: dict[str, str]
    ) -> StripeCustomer:
        self.calls.append(
            ("create_customer", {"email": email, "name": name, **metadata})
        )
        self.customer = StripeCustomer("cus_new", email, name)
        return self.customer

    def create_payment_intent(self, **kwargs: object) -> PaymentIntent:
        self.calls.append(("create_intent", kwargs))
        if self.create_error is not None:
            raise self.create_error
        return PaymentIntent("pi_test", "requires_confirmation", "secret")

    def confirm_payment_intent(
        self, payment_intent_id: str, payment_method: str
    ) -> PaymentIntent:
        self.calls.append(("confirm_intent", payment_intent_id))
        return self.confirmed_intent


class FakePayments:
    def __init__(self, result: PaymentResult) -> None:
        self.result = result

    def pay(self, order: Order, payment_method: str) -> PaymentResult:
        return self.result


class PaymentServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.order = Order("order-42", "ada@example.com", "Ada Lovelace", 2_500)

    def test_new_customer_checkout_is_one_domain_operation(self) -> None:
        stripe = FakeStripe()

        result = PaymentService(stripe).pay(self.order, "pm_card_visa")

        self.assertEqual(result.status, PaymentStatus.COMPLETED)
        self.assertEqual(
            [name for name, _ in stripe.calls],
            ["find_customer", "create_customer", "create_intent", "confirm_intent"],
        )
        intent_arguments = stripe.calls[2][1]
        self.assertEqual(intent_arguments["amount"], 2_500)
        self.assertEqual(intent_arguments["customer_id"], "cus_new")

    def test_existing_customer_is_reused(self) -> None:
        stripe = FakeStripe(StripeCustomer("cus_existing", "ada@example.com", "Ada"))

        PaymentService(stripe).pay(self.order, "pm_card_visa")

        self.assertNotIn("create_customer", [name for name, _ in stripe.calls])
        self.assertEqual(stripe.calls[1][1]["customer_id"], "cus_existing")

    def test_stripe_error_is_translated_to_a_domain_result(self) -> None:
        stripe = FakeStripe(create_error=StripeCardError("Card declined"))

        result = PaymentService(stripe).pay(self.order, "pm_card_declined")

        self.assertEqual(result.status, PaymentStatus.DECLINED)
        self.assertEqual(result.reason, "Card declined")

    def test_customer_action_is_translated_to_a_domain_result(self) -> None:
        stripe = FakeStripe(
            confirmed_intent=PaymentIntent(
                "pi_action", "requires_action", "action-token"
            )
        )

        result = PaymentService(stripe).pay(self.order, "pm_card_authentication")

        self.assertEqual(result.status, PaymentStatus.REQUIRES_CUSTOMER_ACTION)
        self.assertEqual(result.action_token, "action-token")

    def test_application_code_can_use_a_domain_fake(self) -> None:
        payments = FakePayments(
            PaymentResult(PaymentStatus.COMPLETED, payment_id="payment-42")
        )

        message = pay_for_order(payments, self.order, "test-card")

        self.assertEqual(message, "payment complete: payment-42")


if __name__ == "__main__":
    unittest.main(verbosity=2)
