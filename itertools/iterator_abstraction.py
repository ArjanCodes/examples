from dataclasses import dataclass
from typing import Iterable


@dataclass
class LineItem:
    price: int
    quantity: int

    def total(self) -> int:
        return self.price * self.quantity

    def __hash__(self) -> int:
        return hash((self.price, self.quantity))


def print_totals(items: Iterable[LineItem]) -> None:
    for item in items:
        print(item.total())


def main() -> None:
    line_items = {
        LineItem(1, 2),
        LineItem(3, 4),
        LineItem(5, 6),
    }
    print_totals(line_items)


if __name__ == "__main__":
    main()
