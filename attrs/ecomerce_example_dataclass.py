"""Ecommerce modeling with dataclass example."""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Product:
    """Product in ecommerce chart."""

    name: str = field(compare=True)
    category: str = field(compare=True)
    shipping_weight: float = field(compare=False)
    unit_price: int = field(compare=False)
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

    def calculate_sub_total(self) -> int:
        """Total order price without taxes."""
        return sum((p.unit_price for p in self.products))

    def calculate_tax(self) -> float:
        """Total paid in taxes."""
        return sum((p.unit_price * p.tax_percent for p in self.products))

    def calculate_total(self) -> float:
        """Total order price considering taxes."""
        return self.calculate_sub_total() + self.calculate_tax()

    @property
    def total_weight(self) -> float:
        """Total weight of order."""
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
        shipping_weight=2,
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

    order = Order(creation_date=date.today(), status="openned")

    order.add_item(banana)
    order.add_item(mango)
    order.add_item(expensive_mango)

    print(f"Comparison bewteen mango and expensive mango: {mango == expensive_mango}")

    print(f"Total order price: ${order.calculate_total()/100:.2f}")
    print(f"Subtotal order price: ${order.calculate_sub_total()/100:.2f}")
    print(f"Value paid in taxes: ${order.calculate_tax()/100:.2f}")
    print(f"Total weight order: {order.total_weight} kg")


if __name__ == "__main__":
    main()
