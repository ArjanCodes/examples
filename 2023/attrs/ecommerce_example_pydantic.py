from datetime import date
from enum import StrEnum, auto

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class OrderStatus(StrEnum):
    OPEN = auto()
    CLOSED = auto()


class Product(BaseModel):
    name: str
    category: str
    shipping_weight: PositiveFloat
    unit_price: PositiveInt
    tax_percent: float = Field(ge=0, le=1)


class Order(BaseModel):
    status: OrderStatus
    creation_date: date = date.today()
    products: list[Product] = Field(default_factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    @property
    def sub_total(self) -> int:
        return sum((product.unit_price for product in self.products))

    @property
    def tax(self) -> float:
        return sum(
            (product.unit_price * product.tax_percent for product in self.products)
        )

    @property
    def total_price(self) -> float:
        return self.sub_total + self.tax

    @property
    def total_shipping_weight(self) -> float:
        return sum((product.shipping_weight for product in self.products))


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

    order = Order(status=OrderStatus.OPEN)
    for product in [banana, mango, expensive_mango]:
        order.add_product(product)

    print(f"Comparison between mango and expensive mango: {mango == expensive_mango}")
    print(f"Total order price: ${order.total_price / 100:.2f}")
    print(f"Subtotal order price: ${order.sub_total / 100:.2f}")
    print(f"Value paid in taxes: ${order.tax / 100:.2f}")
    print(f"Total weight order: {order.total_shipping_weight} kg")


if __name__ == "__main__":
    main()
