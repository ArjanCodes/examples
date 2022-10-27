from dataclasses import dataclass
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


@dataclass
class Card:
    number: str
    expiry_month: int
    expiry_year: int
    valid: bool = False


@dataclass
class Customer:
    name: str
    phone: str
    card: Card
    card_valid: bool = False


def validate_card(card: Card) -> bool:
    return (
        luhn_checksum(card.number)
        and datetime(card.expiry_year, card.expiry_month, 1) > datetime.now()
    )


def main() -> None:
    # valid card example: 1249190007575069
    alice = Customer(
        name="Alice",
        phone="2341",
        card=Card(number="1249190007575069", expiry_month=1, expiry_year=2023),
    )
    alice.card_valid = validate_card(alice.card)
    print(f"Is Alice's card valid? {alice.card.valid}")
    print(alice)


if __name__ == "__main__":
    main()
