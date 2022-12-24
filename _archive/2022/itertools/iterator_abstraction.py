from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class LineItem:
    price: int
    quantity: int

    def total_price(self) -> int:
        return self.price * self.quantity


def print_totals(items: Iterable[LineItem]) -> None:
    for item in items:
        print(item.total_price())


def main() -> None:
    line_items = {
        LineItem(1, 2),
        LineItem(3, 4),
        LineItem(5, 6),
    }
    print_totals(line_items)


if __name__ == "__main__":
    main()
