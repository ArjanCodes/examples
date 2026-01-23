def apply_discount(price: float, discount: float) -> float:
    # Caller must remember:
    # - price >= 0
    # - discount is a fraction between 0 and 1
    return price * (1.0 - discount)


def main() -> None:
    price = 100.0

    # Works, but relies on discipline
    discounted = apply_discount(price, 0.2)
    print(discounted)  # 80.0

    # Silent bug: discount meant as "20%"
    discounted_wrong = apply_discount(price, 20)
    print(discounted_wrong)  # -1900.0 😬

    # Negative prices are also allowed
    negative = apply_discount(-50.0, 0.1)
    print(negative)  # -45.0 😬


if __name__ == "__main__":
    main()
