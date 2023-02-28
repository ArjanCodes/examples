from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class ProductDescription:
    price: int
    description: str


@dataclass
class SaleLineItem:
    product: ProductDescription
    quantity: int

    @property
    def total_price(self) -> int:
        return self.quantity * self.product.price


@dataclass
class Sale:
    items: list[SaleLineItem] = field(default_factory=list)
    time: datetime = field(default=datetime.now())

    @property
    def total_price(self) -> int:
        return sum((line.quantity * line.product.price for line in self.items))

    def add_line_item(self, product: ProductDescription, quantity: int) -> None:
        self.items.append(SaleLineItem(product, quantity))


def main() -> None:
    headset = ProductDescription(price=5_000, description="Logitech headset")
    keyboard = ProductDescription(price=7_500, description="Reddragon gaming heyboard")

    row1 = SaleLineItem(headset, quantity=2)
    print(f"Price of line 1: ${row1.total_price / 100:.2f}")

    row2 = SaleLineItem(keyboard, quantity=3)
    print(f"Price of line 2: ${row2.total_price / 100:.2f}")

    sale = Sale()
    sale.add_line_item(product=headset, quantity=2)
    sale.add_line_item(product=keyboard, quantity=3)

    print(f"Total price of sale: ${sale.total_price / 100:.2f}")


if __name__ == "__main__":
    main()
