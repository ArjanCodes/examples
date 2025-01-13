from dataclasses import dataclass, field
from enum import Enum


class PaymentStatusError(Exception):
    pass


class PaymentStatus(Enum):
    CANCELLED = "cancelled"
    PENDING = "pending"
    PAID = "paid"


@dataclass
class LineItem:
    name: str
    price: int
    quantity: int = 1

    @property
    def total_price(self) -> int:
        return self.price * self.quantity


@dataclass
class Order:
    items: list[LineItem] = field(default_factory=list)
    _payment_status: PaymentStatus = PaymentStatus.PENDING

    def add_item(self, item: LineItem):
        self.items.append(item)

    def get_payment_status(self) -> PaymentStatus:
        return self._payment_status

    def set_payment_status(self, status: PaymentStatus) -> None:
        # here, using a (getter +) setter is okay, because we're doing something
        # more than just setting the value
        if self._payment_status == PaymentStatus.PAID:
            raise PaymentStatusError(
                "You can't change the status of an already paid order."
            )
        self._payment_status = status

    @property
    def total_price(self) -> int:
        return sum(item.total_price for item in self.items)


def main():
    order = Order()
    order.add_item(LineItem("carrots", price=20, quantity=10))
    order.add_item(LineItem("self-raising flower", price=200))
    order.add_item(LineItem("eggs", price=20, quantity=5))
    order.add_item(LineItem("gingerbread spices", price=189))
    order.add_item(LineItem("sunflower oil", price=169))
    order.add_item(LineItem("brown sugar", price=99))
    order.add_item(LineItem("lemon", price=25))
    order.add_item(LineItem("ginger", price=79))
    order.add_item(LineItem("raisins", price=159))
    order.add_item(LineItem("powdered sugar", price=89))
    order.add_item(LineItem("cream cheese", price=219, quantity=2))

    print(f"Total price: ${order.total_price / 100:.2f}")


if __name__ == "__main__":
    main()
