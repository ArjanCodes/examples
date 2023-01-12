from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar

Cents = TypeVar("Cents", bound=int)


@dataclass
class ProductDescription:
    price: Cents
    description: str


@dataclass
class SaleLineItem:
    product: ProductDescription
    quantity: int


@dataclass
class Sale:
    items: list[SaleLineItem] = field(default_factory=list)
    time: datetime = field(default=datetime.now())


def main() -> None:
    headset = ProductDescription(price=5_000, description="Gaming headset")
    keyboard = ProductDescription(price=7_500, description="Mechanical gaming keyboard")

    row1 = SaleLineItem(product=headset, quantity=2)
    row2 = SaleLineItem(product=keyboard, quantity=3)

    sale = Sale([row1, row2])

    print(sale)


if __name__ == "__main__":
    main()
