from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class ProductDescription:
    """Product information."""

    price: int
    description: str


@dataclass
class SaleLineItem:
    """One record in an sale."""

    product: ProductDescription
    quantity: int

    def total_line_price(self) -> int:
        """Returns the total of one line in the sale."""
        return self.quantity * self.product.price


@dataclass
class Cash:
    """Payment method using cash."""

    discount: float = 0.1


@dataclass
class CreditCard:
    """Payment method using credit card."""

    number: str
    tax: float = 0.1


@dataclass
class Sale:
    """A sale to store all line records within it."""

    items: list[SaleLineItem] = field(default_factory=list)
    time: datetime = field(default=datetime.now())

    @property
    def total_price(self) -> int:
        """Returns the total price of the sale."""
        return sum((line.quantity * line.product.price for line in self.items))

    def add_line_item(self, product: ProductDescription, quantity: int) -> None:
        """Adds an product to the sale line."""
        self.items.append(SaleLineItem(product, quantity))

    def total_discounted_price(self, payment_method: Cash | CreditCard) -> float:
        """Calculates the net price of sale."""
        if isinstance(payment_method, Cash):
            return self.total_price * (1 - payment_method.discount)
        else:
            return self.total_price * (1 + payment_method.tax)


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
