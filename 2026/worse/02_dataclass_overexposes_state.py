from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class ShoppingCart:
    # Every field becomes part of the public mutation API.
    items: list[Decimal] = field(default_factory=list[Decimal])
    discount: Decimal = Decimal(0)


class SaferShoppingCart:
    def __init__(self) -> None:
        self._items: list[Decimal] = []
        self._discount = Decimal(0)

    def add_item(self, price: Decimal) -> None:
        if price <= 0:
            raise ValueError("An item price must be positive")
        self._items.append(price)

    def apply_discount(self, discount: Decimal) -> None:
        if not Decimal(0) <= discount <= Decimal(1):
            raise ValueError("Discount must be between 0 and 1")
        self._discount = discount

    @property
    def total(self) -> Decimal:
        return sum(self._items, start=Decimal(0)) * (Decimal(1) - self._discount)


def main() -> None:
    cart = ShoppingCart()
    cart.discount = Decimal(2)  # Valid Python; nonsensical business state.
    print(f"Overexposed cart discount: {cart.discount}")

    safer_cart = SaferShoppingCart()
    safer_cart.add_item(Decimal("19.99"))
    safer_cart.apply_discount(Decimal("0.10"))
    print(f"Protected cart total: {safer_cart.total}")


if __name__ == "__main__":
    main()
