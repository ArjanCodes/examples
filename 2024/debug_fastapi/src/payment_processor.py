def process_payment(amount: int | float, discount_percent: int) -> int | float:
    discounted_price = calculate_discounted_price(amount, discount_percent)
    print(f"Original Amount: ${amount:.2f}")
    print(f"Discount: {discount_percent}%")
    print(f"Final Charged Amount: ${discounted_price:.2f}")
    return discounted_price


def calculate_discounted_price(
    amount: int | float, discount_percent: int
) -> int | float:
    discount = amount * (discount_percent / 100)

    final_amount = round(amount - discount, 2)  # final_amount = amount - discount

    return final_amount
