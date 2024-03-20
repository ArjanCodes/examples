from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


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
    exp_month: int
    exp_year: int
    valid: bool = False


@dataclass
class Customer:
    name: str
    phone: str
    card: Card
    card_valid: bool = False


class CardInfo(Protocol):
    @property
    def number(self) -> str: ...

    @property
    def exp_month(self) -> int: ...

    @property
    def exp_year(self) -> int: ...


def validate_card(card: CardInfo) -> bool:
    return (
        luhn_checksum(card.number)
        and datetime(card.exp_year, card.exp_month, 1) > datetime.now()
    )


def main() -> None:
    card = Card(number="1249190007575069", exp_month=1, exp_year=2024)
    alice = Customer(name="Alice", phone="2341", card=card)
    card.valid = validate_card(card)
    print(f"Is Alice's card valid? {card.valid}")
    print(alice)


if __name__ == "__main__":
    main()
