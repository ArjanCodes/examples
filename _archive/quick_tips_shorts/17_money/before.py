VAT = 0.18


PRICES = {
    "burger": 9.99,
    "fries": 4.99,
    "drink": 1.99,
    "salad": 14.99,
}


def order_food(items: list[str]) -> None:
    total = sum(PRICES[item] for item in items)
    vat = total * VAT
    total += vat
    print(f"Your order is ${total} (VAT: ${vat}).")
    print("Thanks for your business!")


def main() -> None:
    order_food(["burger", "salad", "fries"])


if __name__ == "__main__":
    main()
