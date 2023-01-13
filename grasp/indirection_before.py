from __future__ import annotations

from dataclasses import dataclass
from datetime import date

YEAR = 360
HALF_YEAR = int(YEAR / 2)


@dataclass
class Order:
    """Represents and order in an e-commerce system."""

    customer: Customer

    def get_discount(self) -> float:
        """Returns the discount for the order."""
        return self.customer.get_discount()


@dataclass
class Customer:
    """Represents a client."""

    since: date

    @property
    def lifetime_days(self) -> int:
        """Returns how long the person has been a customer in days."""
        return (date.today() - self.since).days

    def get_discount(self) -> float:
        """Returns the discount based on how long the person has been a client."""
        if self.lifetime_days < HALF_YEAR:
            return 0.0
        elif HALF_YEAR <= self.lifetime_days < YEAR:
            return 0.1
        elif YEAR <= self.lifetime_days < YEAR * 2:
            return 0.15
        else:
            return 0.2


def main() -> None:

    henry = Customer(since=date(2023, 1, 1))
    order1 = Order(henry)
    print(f"Henry got {order1.get_discount() * 100:.0f} % discount")

    anthony = Customer(since=date(2018, 1, 1))
    order2 = Order(anthony)
    print(f"Anthony got {order2.get_discount() * 100:.0f} % discount")


if __name__ == "__main__":
    main()
