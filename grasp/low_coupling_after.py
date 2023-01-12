from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar

Cents = TypeVar("Cents", bound=int)


@dataclass(kw_only=True)
class ProductDescription:
    price: Cents
    description: str


@dataclass
class SaleLineItem:
    product: ProductDescription
    quantity: int

    def total_line_price(self) -> int:
        return self.quantity * self.product.price


@dataclass
class Cash:
    discount: float = 0.1


@dataclass
class CreditCard:
    number: str
    tax: float = 0.05


@dataclass
class Sale:
    items: list[SaleLineItem] = field(default_factory=list)
    time: datetime = field(default=datetime.now())

    def calculate_total_price(self) -> int:
        return sum((line.quantity * line.product.price for line in self.items))

    def add_line_item(self, product: ProductDescription, quantity: int) -> None:
        self.items.append(SaleLineItem(product, quantity))

    def calculate_payment(self, payment_methd) -> float:

        if isinstance(payment_methd, Cash):
            return self.calculate_total_price() * (1 - payment_methd.discount)

        elif isinstance(payment_methd, CreditCard):
            return self.calculate_total_price() * (1 + payment_methd.tax)


def main() -> None:
    headset = ProductDescription(price=5_000, description="Logitech headset")
    keyboard = ProductDescription(price=7_500, description="Reddragon gaming heyboard")

    row1 = SaleLineItem(headset, quantity=2)
    print(f"Price of line 1: ${row1.total_line_price() / 100:.2f}")

    row2 = SaleLineItem(keyboard, quantity=3)
    print(f"Price of line 2: ${row2.total_line_price() / 100:.2f}")

    sale = Sale()
    sale.add_line_item(product=headset, quantity=1)
    sale.add_line_item(product=keyboard, quantity=1)

    print(f"Total price of sale: ${sale.calculate_total_price() / 100:.2f}")

    cc = CreditCard("123456789")
    cash = Cash()
    print(f"Final value paid in cc: ${sale.calculate_payment(cc) / 100:.2f}")
    print(f"Final value paid in cash: ${sale.calculate_payment(cash) / 100:.2f}")


if __name__ == "__main__":
    main()
