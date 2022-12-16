"""Ecommerce modeling with dataclass example."""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Product:
    """Product in ecommerce chart."""

    name: str = field(compare=True)
    category: str = field(compare=True)
    shipping_weight: float = field(compare=False)
    unit_price: float = field(compare=False)
    tax_percent: float = field(compare=False)

    def __post_init__(self) -> None:
        if self.unit_price < 0:
            raise ValueError("unit_price attribute must greater then zero.")

        if self.shipping_weight < 0:
            raise ValueError("shipping_weight attribute must greater then zero.")

        if not 0 < self.tax_percent < 1:
            raise ValueError("tax_percent attribute must be between zero and one.")


@dataclass
class Order:
    """Order in ecommerce website."""

    status: str
    creation_date: date = date.today()
    products: list[Product] = field(default_factory=list)

    def add_item(self, product: Product) -> None:
        """Insert one product into order."""
        self.products.append(product)

    def calculate_sub_total(self) -> float:
        """Total order price without taxes."""
        subtotal = sum((p.unit_price for p in self.products))
        return round(subtotal, 2)

    def calculate_tax(self) -> float:
        """Total paid in taxes."""
        taxes = sum((p.unit_price * p.tax_percent for p in self.products))
        return round(taxes, 2)

    def calculate_total(self) -> float:
        """Total order price considering taxes."""
        total = self.calculate_sub_total() + self.calculate_tax()
        return round(total, 2)

    @property
    def total_weight(self) -> float:
        """Total weight of order."""
        return sum((p.shipping_weight for p in self.products))


def main() -> None:
    banana = Product(
        name="banana",
        category="fruit",
        shipping_weight=0.5,
        unit_price=2.15,
        tax_percent=0.07,
    )

    mango = Product(
        name="mango",
        category="fruit",
        shipping_weight=2,
        unit_price=3.19,
        tax_percent=0.11,
    )

    order = Order(creation_date=date.today(), status="openned")

    order.add_item(banana)
    order.add_item(mango)

    print(f"Total order price: U$ {order.calculate_total()}")
    print(f"Subtotal order price: U$ {order.calculate_sub_total()}")
    print(f"Value paid in taxes: U$ {order.calculate_tax()}")
    print(f"Total weight order: {order.total_weight}")


if __name__ == "__main__":
    main()
