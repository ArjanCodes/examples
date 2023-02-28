from __future__ import annotations

from datetime import date
from enum import StrEnum, auto

from attrs import Attribute, define, field, validators


class OrderStatus(StrEnum):
    OPEN = auto()
    CLOSED = auto()


def positive_number(
    instance: type, attribute: Attribute[str], value: int | float
) -> None:
    """Custom check whether an attribute of an instance has a positive value assingned."""
    class_name = instance.__class__.__name__
    if value <= 0:
        raise ValueError(
            f"{class_name} {attribute.name} attribute must be greater then zero."
        )


def percentage_value(instance: type, attribute: Attribute[str], value: float) -> None:
    """Custom check whether an attribute of an instance has a percentage assigned."""
    class_name = instance.__class__.__name__
    if not 0 <= value <= 1:
        raise ValueError(
            f"{class_name} {attribute.name} attribute must be between 0 and 1."
        )


@define
class Product:
    name: str = field(eq=str.lower)
    category: str = field(eq=str.lower)
    shipping_weight: float = field(
        validator=[validators.instance_of(float), positive_number], eq=False
    )
    unit_price: int = field(
        validator=[validators.instance_of(int), positive_number], eq=False
    )
    tax_percent: float = field(
        validator=[validators.instance_of(float), percentage_value], eq=False
    )


@define(kw_only=True)
class Order:
    status: OrderStatus
    creation_date: date = date.today()
    products: list[Product] = field(factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    @property
    def sub_total(self) -> int:
        return sum((p.unit_price for p in self.products))

    @property
    def tax(self) -> float:
        return sum((p.unit_price * p.tax_percent for p in self.products))

    @property
    def total_price(self) -> float:
        return self.sub_total + self.tax

    @property
    def total_shipping_weight(self) -> float:
        return sum((p.shipping_weight for p in self.products))


def main() -> None:
    banana = Product(
        name="banana",
        category="fruit",
        shipping_weight=0.5,
        unit_price=215,
        tax_percent=0.07,
    )

    mango = Product(
        name="mango",
        category="fruit",
        shipping_weight=2.0,
        unit_price=319,
        tax_percent=0.11,
    )

    expensive_mango = Product(
        name="Mango",
        category="Fruit",
        shipping_weight=4.0,
        unit_price=800,
        tax_percent=0.20,
    )

    order = Order(status=OrderStatus.OPEN)
    for product in [banana, mango, expensive_mango]:
        order.add_product(product)

    print(f"Comparison between mango and expensive mango: {mango == expensive_mango}")
    print(f"Total order price: ${order.total_price/100:.2f}")
    print(f"Subtotal order price: ${order.sub_total/100:.2f}")
    print(f"Value paid in taxes: ${order.tax/100:.2f}")
    print(f"Total weight order: {order.total_shipping_weight} kg")


if __name__ == "__main__":
    main()
