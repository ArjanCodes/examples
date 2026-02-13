from dataclasses import dataclass
from typing import Protocol


class PaymentState(Protocol):
    """Common interface for all states."""

    def authorize(self, payment: "Payment") -> None: ...
    def capture(self, payment: "Payment") -> None: ...
    def fail(self, payment: "Payment") -> None: ...
    def refund(self, payment: "Payment") -> None: ...


@dataclass
class Payment:
    """The Context: delegates behavior to the current state."""

    payment_id: str
    audit: list[str]
    state: PaymentState

    def authorize(self) -> None:
        self.state.authorize(self)

    def capture(self) -> None:
        self.state.capture(self)

    def fail(self) -> None:
        self.state.fail(self)

    def refund(self) -> None:
        self.state.refund(self)


# ---------- Concrete States ----------


class New:
    def authorize(self, payment: Payment) -> None:
        payment.audit.append(f"{payment.payment_id}: authorized")
        payment.state = Authorized()

    def capture(self, payment: Payment) -> None:
        raise RuntimeError("Cannot capture before authorize")

    def fail(self, payment: Payment) -> None:
        payment.audit.append(f"{payment.payment_id}: failed")
        payment.state = Failed()

    def refund(self, payment: Payment) -> None:
        raise RuntimeError("Cannot refund a new payment")


class Authorized:
    def authorize(self, payment: Payment) -> None:
        raise RuntimeError("Already authorized")

    def capture(self, payment: Payment) -> None:
        payment.audit.append(f"{payment.payment_id}: captured")
        payment.state = Captured()

    def fail(self, payment: Payment) -> None:
        payment.audit.append(f"{payment.payment_id}: failed")
        payment.state = Failed()

    def refund(self, payment: Payment) -> None:
        payment.audit.append(f"{payment.payment_id}: refunded")
        payment.state = Refunded()


class Captured:
    def authorize(self, payment: Payment) -> None:
        raise RuntimeError("Already captured")

    def capture(self, payment: Payment) -> None:
        raise RuntimeError("Already captured")

    def fail(self, payment: Payment) -> None:
        raise RuntimeError("Cannot fail after capture")

    def refund(self, payment: Payment) -> None:
        payment.audit.append(f"{payment.payment_id}: refunded")
        payment.state = Refunded()


class Failed:
    def authorize(self, payment: Payment) -> None:
        raise RuntimeError("Cannot authorize a failed payment")

    def capture(self, payment: Payment) -> None:
        raise RuntimeError("Cannot capture a failed payment")

    def fail(self, payment: Payment) -> None:
        raise RuntimeError("Already failed")

    def refund(self, payment: Payment) -> None:
        raise RuntimeError("Nothing to refund")


class Refunded:
    def authorize(self, payment: Payment) -> None:
        raise RuntimeError("Refunded payments stay refunded")

    def capture(self, payment: Payment) -> None:
        raise RuntimeError("Refunded payments stay refunded")

    def fail(self, payment: Payment) -> None:
        raise RuntimeError("Refunded payments stay refunded")

    def refund(self, payment: Payment) -> None:
        raise RuntimeError("Already refunded")


# ---------- Demo ----------


def main() -> None:
    p = Payment(payment_id="p1", audit=[], state=New())

    p.authorize()
    p.capture()
    p.refund()

    print("final state:", type(p.state).__name__)
    print("audit:", p.audit)


if __name__ == "__main__":
    main()
