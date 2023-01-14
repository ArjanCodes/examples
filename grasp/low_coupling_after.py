from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol


@dataclass(kw_only=True)
class ProductDescription:
    price: int
    description: str


@dataclass
class SaleLineItem:
    product: ProductDescription
    quantity: int

    def total_line_price(self) -> int:
        return self.quantity * self.product.price


class PaymentMethod(Protocol):
    def net_price(self, total_price: int) -> int:
        ...


@dataclass
class Cash(PaymentMethod):
    percentage: float = 0.1

    def net_price(self, total_price: int) -> int:
        return total_price * (1 - self.percentage)


@dataclass
class CreditCard:
    number: str
    percentage: float = 0.05

    def net_price(self, total_price: int) -> int:
        return total_price * (1 + self.percentage)


@dataclass
class Sale:
    items: list[SaleLineItem] = field(default_factory=list)
    time: datetime = field(default=datetime.now())

    @property
    def total_price(self) -> int:
        return sum((line.quantity * line.product.price for line in self.items))

    def add_line_item(self, product: ProductDescription, quantity: int) -> None:
        self.items.append(SaleLineItem(product, quantity))

    def total_discounted_price(self, payment_methd: PaymentMethod) -> int:
        return payment_methd.net_price(self.total_price)


def main() -> None:
    headset = ProductDescription(price=5_000, description="Logitech headset")
    keyboard = ProductDescription(price=7_500, description="Reddragon gaming heyboard")

    row1 = SaleLineItem(headset, quantity=2)
    print(f"Price of line 1: ${row1.total_line_price() / 100:.2f}")

    row2 = SaleLineItem(keyboard, quantity=3)
    print(f"Price of line 2: ${row2.total_line_price() / 100:.2f}")

    sale = Sale()
    sale.add_line_item(product=headset, quantity=2)
    sale.add_line_item(product=keyboard, quantity=3)

    print(f"Total price of sale: ${sale.total_price / 100:.2f}")

    cc = CreditCard("123456789")
    cash = Cash()
    print(f"Final value paid in cc: ${sale.total_discounted_price(cc) / 100:.2f}")
    print(f"Final value paid in cash: ${sale.total_discounted_price(cash) / 100:.2f}")


if __name__ == "__main__":
    main()
