from dataclasses import dataclass, field
from enum import Enum, auto

from sm import StateMachine


class PayState(Enum):
    NEW = auto()
    AUTHORIZED = auto()
    CAPTURED = auto()
    FAILED = auto()
    REFUNDED = auto()


class PayEvent(Enum):
    AUTHORIZE = auto()
    CAPTURE = auto()
    FAIL = auto()
    REFUND = auto()


@dataclass
class PaymentCtx:
    payment_id: str
    audit: list[str] = field(default_factory=list[str])


# Create the machine
pay_sm: StateMachine[PayState, PayEvent, PaymentCtx] = StateMachine()


# ----- Define transition actions -----


def authorize(ctx: PaymentCtx) -> None:
    ctx.audit.append(f"{ctx.payment_id}: authorized")


def capture(ctx: PaymentCtx) -> None:
    ctx.audit.append(f"{ctx.payment_id}: captured")


def fail(ctx: PaymentCtx) -> None:
    ctx.audit.append(f"{ctx.payment_id}: failed")


def refund(ctx: PaymentCtx) -> None:
    ctx.audit.append(f"{ctx.payment_id}: refunded")


# ----- Register transitions explicitly -----

pay_sm.add_transition(
    PayState.NEW,
    PayEvent.AUTHORIZE,
    PayState.AUTHORIZED,
    authorize,
)

pay_sm.add_transition(
    PayState.NEW,
    PayEvent.FAIL,
    PayState.FAILED,
    fail,
)

pay_sm.add_transition(
    PayState.AUTHORIZED,
    PayEvent.CAPTURE,
    PayState.CAPTURED,
    capture,
)

pay_sm.add_transition(
    PayState.AUTHORIZED,
    PayEvent.FAIL,
    PayState.FAILED,
    fail,
)

pay_sm.add_transition(
    PayState.AUTHORIZED,
    PayEvent.REFUND,
    PayState.REFUNDED,
    refund,
)

pay_sm.add_transition(
    PayState.CAPTURED,
    PayEvent.REFUND,
    PayState.REFUNDED,
    refund,
)


@dataclass
class Payment:
    ctx: PaymentCtx
    state: PayState = PayState.NEW

    def handle(self, event: PayEvent) -> None:
        self.state = pay_sm.handle(self.ctx, self.state, event)


def main():
    p = Payment(ctx=PaymentCtx("p1"))

    p.handle(PayEvent.AUTHORIZE)
    p.handle(PayEvent.CAPTURE)
    p.handle(PayEvent.REFUND)

    print("state:", p.state)
    print("audit:", p.ctx.audit)


if __name__ == "__main__":
    main()
