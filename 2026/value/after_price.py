from typing import Any, Self


class Price(float):
    """Validated float representing a non-negative price."""

    def __new__(cls, value: Any) -> Self:
        val = float(value)
        if val < 0:
            raise ValueError("Price must be non-negative")
        return super().__new__(cls, val)


class Percentage(float):
    """Validated float representing a fraction between 0 and 1."""

    def __new__(cls, value: Any) -> Self:
        val = float(value)
        if not 0.0 <= val <= 1.0:
            raise ValueError("Percentage must be between 0 and 1")
        return super().__new__(cls, val)

    @classmethod
    def from_percent(cls, value: Any) -> Self:
        return cls(float(value) / 100.0)


def apply_discount(price: Price, discount: Percentage) -> Price:
    return Price(price * (1.0 - discount))


def main() -> None:
    price = Price(100.0)

    # Explicit and safe
    discount = Percentage.from_percent(20)
    discounted = apply_discount(price, discount)
    print(discounted)  # 80.0

    # All of these now fail early and loudly:
    # Price(-50)
    # Percentage(20)
    # apply_discount(price, Percentage(-0.1))


if __name__ == "__main__":
    main()
