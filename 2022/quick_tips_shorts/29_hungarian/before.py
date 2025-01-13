VAT = 0.18


PRICES = {
    "burger": 9_99,
    "fries": 4_99,
    "drink": 1_99,
    "salad": 14_99,
}


def fn_order_food(rgs_items: list[str]) -> None:
    i_total = sum(PRICES[item] for item in rgs_items)
    i_vat = int(i_total * VAT)
    i_total += i_vat
    print(f"Your order is ${i_total / 100:.2f} (VAT: ${i_vat / 100:.2f}).")
    print("Thanks for your business!")


def fn_main() -> None:
    fn_order_food(["burger", "salad", "fries"])


if __name__ == "__main__":
    fn_main()
