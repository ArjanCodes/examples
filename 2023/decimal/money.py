from dataclasses import dataclass
from decimal import Decimal
from typing import Self


@dataclass
class Money:
    amount_cents: int = 0
    currency_symbol: str = "$"

    @classmethod
    def mint(cls, amount: Decimal | float, currency_symbol: str = "$") -> Self:
        return cls(int(amount * 100), currency_symbol)

    def __str__(self):
        dollars = self.amount_cents // 100
        cents = self.amount_cents % 100
        return f"{self.currency_symbol}{dollars}.{cents:02d}"

    def __add__(self, other: Self) -> Self:
        if isinstance(other, Money):
            return Money(self.amount_cents + other.amount_cents, self.currency_symbol)

    def __sub__(self, other: Self) -> Self:
        if isinstance(other, Money):
            return Money(self.amount_cents - other.amount_cents, self.currency_symbol)


def main() -> None:
    # Create Money instances with different currency symbols
    balance = Money.mint(100)  # US Dollar
    withdrawal = Money.mint(42.37)
    deposit = Money.mint(0.10)

    # Perform arithmetic operations
    result = balance - withdrawal + deposit

    # Display the result
    print("Using Money class:")
    print(f"{balance} - {withdrawal} + {deposit} = {result}")

    # Example with a different currency
    balance_euro = Money.mint(100, "€")  # Euro
    withdrawal_euro = Money.mint(42.37, "€")
    deposit_euro = Money.mint(0.10, "€")

    result_euro = balance_euro - withdrawal_euro + deposit_euro
    print("\nUsing Money class with another currency symbol:")
    print(f"{balance_euro} - {withdrawal_euro} + {deposit_euro} = {result_euro}")


if __name__ == "__main__":
    main()
