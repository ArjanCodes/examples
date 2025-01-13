VAT = 0.18


PRICES = {
    "burger": 9_99,
    "fries": 4_99,
    "drink": 1_99,
    "salad": 14_99,
}


def order_food(items: list[str]) -> None:
    total = sum(PRICES[item] for item in items)
    vat = int(total * VAT)
    total += vat
    print(f"Your order is ${total / 100:.2f} (VAT: ${vat / 100:.2f}).")
    print("Thanks for your business!")


def main() -> None:
    order_food(["burger", "salad", "fries"])


if __name__ == "__main__":
    main()
