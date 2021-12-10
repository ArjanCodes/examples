from dataclasses import dataclass
from enum import Enum
from typing import Any


class PaymentStatus(Enum):
    CANCELLED = "cancelled"
    PENDING = "pending"
    PAID = "paid"


class PaymentStatusError(Exception):
    pass


@dataclass
class OrderNoEncapsulationNoInformationHiding:
    """Anyone can get the payment status directly via the instance variable.
    There are no boundaries whatsoever."""

    payment_status: PaymentStatus = PaymentStatus.PENDING


@dataclass
class OrderEncapsulationNoInformationHiding:
    """There's an interface now that you should use that provides encapsulation.
    Users of this class still need to know that the status is represented by an enum type."""

    _payment_status: PaymentStatus = PaymentStatus.PENDING

    def get_payment_status(self) -> PaymentStatus:
        return self._payment_status

    def set_payment_status(self, status: PaymentStatus) -> None:
        if self._payment_status == PaymentStatus.PAID:
            raise PaymentStatusError(
                "You can't change the status of an already paid order."
            )
        self._payment_status = status


@dataclass
class OrderEncapsulationAndInformationHiding:
    """The status variable is set to 'private'. The only thing you're supposed to use is the is_paid
    method, you need no knowledge of how status is represented (that information is 'hidden')."""

    _payment_status: PaymentStatus = PaymentStatus.PENDING

    def is_paid(self) -> bool:
        return self._payment_status == PaymentStatus.PAID

    def is_cancelled(self) -> bool:
        return self._payment_status == PaymentStatus.CANCELLED

    def cancel(self) -> None:
        if self._payment_status == PaymentStatus.PAID:
            raise PaymentStatusError("You can't cancel an already paid order.")
        self._payment_status = PaymentStatus.CANCELLED

    def pay(self):
        if self._payment_status == PaymentStatus.PAID:
            raise PaymentStatusError("Order is already paid.")
        self._payment_status = PaymentStatus.PAID


@dataclass
class OrderInformationHidingWithoutEncapsulation:
    """The status variable is public again (so there's no boundary),
    but we don't know what the type is - that information is hidden."""

    payment_status: Any = None

    def is_paid(self) -> bool:
        return self.payment_status == PaymentStatus.PAID

    def is_cancelled(self) -> bool:
        return self.payment_status == PaymentStatus.CANCELLED

    def cancel(self) -> None:
        if self.payment_status == PaymentStatus.PAID:
            raise PaymentStatusError("You can't cancel an already paid order.")
        self.payment_status = PaymentStatus.CANCELLED

    def pay(self):
        if self.payment_status == PaymentStatus.PAID:
            raise PaymentStatusError("Order is already paid.")
        self.payment_status = PaymentStatus.PAID


def main():
    test = OrderInformationHidingWithoutEncapsulation()
    test.pay()
    print("Is paid: ", test.is_paid())


if __name__ == "__main__":
    main()
