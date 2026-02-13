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


# Create an instance: this is "the machine"
pay_sm: StateMachine[PayState, PayEvent, PaymentCtx] = StateMachine()


@pay_sm.transition(PayState.NEW, PayEvent.AUTHORIZE, PayState.AUTHORIZED)
def authorize(ctx: PaymentCtx) -> None:
    ctx.audit.append(f"{ctx.payment_id}: authorized")


@pay_sm.transition((PayState.NEW, PayState.AUTHORIZED), PayEvent.FAIL, PayState.FAILED)
def fail(ctx: PaymentCtx) -> None:
    ctx.audit.append(f"{ctx.payment_id}: failed")


@pay_sm.transition(PayState.AUTHORIZED, PayEvent.CAPTURE, PayState.CAPTURED)
def capture(ctx: PaymentCtx) -> None:
    ctx.audit.append(f"{ctx.payment_id}: captured")


@pay_sm.transition(
    (PayState.AUTHORIZED, PayState.CAPTURED), PayEvent.REFUND, PayState.REFUNDED
)
def refund(ctx: PaymentCtx) -> None:
    ctx.audit.append(f"{ctx.payment_id}: refunded")


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

    # Uncomment to see an invalid transition:
    # p2 = Payment(ctx=PaymentCtx("p2", []))
    # p2.handle(PayEvent.CAPTURE)


if __name__ == "__main__":
    main()
