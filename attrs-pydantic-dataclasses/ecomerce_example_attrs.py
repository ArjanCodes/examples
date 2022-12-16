"""Ecommerce modeling with attrs example."""

from datetime import date

from attrs import define, field, validators


def positive_number(instance, attribute, value):
    """Custom check whether an attribute of an instance has a positive value assingned."""
    if value <= 0:
        raise ValueError(f"{attribute} must be greater then zero.")


def percentage_value(instance, attribute, value):
    """Custom check whether an attribute of an instance has a percentage assigned."""
    if not 0 < value < 1:
        raise ValueError(f"{attribute} must be between zero and one.")


@define
class Customer:
    """Customer's information"""

    name: str
    city: str
    country: str


@define
class Product:
    """Product in ecommerce chart."""

    name: str
    category: str
    shipping_weight: float = field(
        validator=[validators.instance_of(float), positive_number]
    )
    unit_price: float = field(
        validator=[validators.instance_of(float), positive_number]
    )
    tax_percent: float = field(
        validator=[validators.instance_of(float), percentage_value]
    )


@define(kw_only=True)
class Order:
    """Order in ecommerce website."""

    date: date
    status: str
    customer: Customer
    products: list[Product] = field(factory=list)

    def add_item(self, product: Product):
        """Insert one product into order."""
        self.products.append(product)

    def calculate_sub_total(self):
        """Total order price without taxes."""
        subtotal = sum((p.unit_price for p in self.products))
        return round(subtotal, 2)

    def calculate_tax(self):
        """Total paid in taxes."""
        taxes = sum((p.unit_price * p.tax_percent for p in self.products))
        return round(taxes, 2)

    def calculate_total(self):
        """Total order price considering taxes."""
        total = self.calculate_sub_total() + self.calculate_tax()
        return round(total, 2)

    @property
    def total_weight(self):
        """Total weight of order."""
        return sum((p.shipping_weight for p in self.products))


if __name__ == "__main__":

    henry = Customer("Henrique", "Sao Jose do Rio Preto", "Brazil")

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
        shipping_weight=2.0,
        unit_price=3.19,
        tax_percent=0.11,
    )

    order = Order(date=date.today(), status="openned", customer=henry)

    order.add_item(banana)
    order.add_item(mango)

    print(f"Total order price: U$ {order.calculate_total()}")
    print(f"Subtotal order price: U$ {order.calculate_sub_total()}")
    print(f"Value paid in taxes: U$ {order.calculate_tax()}")
    print(f"Total weight order: {order.total_weight}")
