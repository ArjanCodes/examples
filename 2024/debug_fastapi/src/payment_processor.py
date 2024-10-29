def process_payment(amount: int, discount_percent: int) -> int:
    discounted_price = calculate_discounted_price(amount, discount_percent)
    print(f"Original Amount: ${amount:.2f}")
    print(f"Discount: {discount_percent}%")
    print(f"Final Charged Amount: ${discounted_price:.2f}")
    return discounted_price


def calculate_discounted_price(amount: int, discount_percent: int) -> int:
    discount = amount * (discount_percent / 100)

    final_amount = amount - discount  # final_amount = round(amount - discount, 2)

    return final_amount
