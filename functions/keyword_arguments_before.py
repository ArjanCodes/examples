from datetime import datetime


def luhn_checksum(card_number: str) -> bool:
    def digits_of(number: str) -> list[int]:
        return [int(d) for d in number]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for digit in even_digits:
        checksum += sum(digits_of(str(digit * 2)))
    return checksum % 10 == 0


def validate_card(card_number: str, expiry_month: int, expiry_year: int) -> bool:
    return (
        luhn_checksum(card_number)
        and datetime(expiry_year, expiry_month, 1) > datetime.now()
    )


def main() -> None:
    card_valid = validate_card(
        "1249190007575069",
        1,
        2023,
    )
    print(f"Is the card valid? {card_valid}")


if __name__ == "__main__":
    main()
