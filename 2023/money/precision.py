from decimal import Decimal


def to_dollars(amount: int) -> str:
    return f"${amount / 100:.2f}"


def main() -> None:
    float_balance = 100.0
    float_withdrawal = 42.37
    float_deposit = 0.1

    float_result = float_balance - float_withdrawal + float_deposit
    print(f"Using float: {float_result}")

    decimal_balance = Decimal("100.00")
    decimal_withdrawal = Decimal("42.37")
    decimal_deposit = Decimal("0.1")

    decimal_result = decimal_balance - decimal_withdrawal + decimal_deposit
    print(f"Using decimal: {decimal_result}")

    int_balance = 10000
    int_withdrawal = 4237
    int_deposit = 10

    int_result = int_balance - int_withdrawal + int_deposit
    print(f"Using integers: {int_result/100:.2f}")


if __name__ == "__main__":
    main()
