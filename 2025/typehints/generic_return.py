from collections.abc import Iterable


def calculate_discounts(items: Iterable[float], discount: float) -> Iterable[float]:
    return [item * (1 - discount) for item in items]


def main() -> None:
    items = [100, 200, 300]
    discount = 0.2
    discounted_items = calculate_discounts(items, discount)
    print(len(discounted_items))  # type issue here
    print(discounted_items[0])  # type issue here


if __name__ == "__main__":
    main()
