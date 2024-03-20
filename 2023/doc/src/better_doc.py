"""Bank account operations using OOP."""

from __future__ import annotations  # * To allow type hints

from datetime import datetime
from enum import StrEnum, auto


class TransactionType(StrEnum):
    DEPOSIT = auto()
    WITHDRAWAL = auto()
    TRANSFER = auto()


Transaction = tuple[TransactionType, datetime, int]


class InsufficientBalanceError(Exception): ...


class BankAccount:
    # TODO: insert docstring
    def __init__(self, initial_balance=0) -> None:
        self._balance = initial_balance
        self._transaction_history: list[Transaction] = []

    def deposit(self, amount) -> None:
        self._balance += amount
        self._transaction_history.append(
            (TransactionType.DEPOSIT, datetime.now(), amount)
        )

    def withdraw(self, amount) -> None:
        if self._sufficient_balance(amount):
            self._balance -= amount
            self._transaction_history.append(
                (TransactionType.WITHDRAWAL, datetime.now(), amount)
            )
        else:
            raise InsufficientBalanceError

    def transfer(self, other, amount) -> None:
        if self._sufficient_balance(amount):
            timestamp: datetime = datetime.now()
            self._balance -= amount
            other._balance += amount
            # ! Can't append operation at other instance class
            self._transaction_history.append(
                (TransactionType.TRANSFER, timestamp, amount)
            )
        else:
            raise InsufficientBalanceError

    def _sufficient_balance(self, amount) -> bool:
        return amount <= self._balance

    @property
    def balance(self) -> int:
        return self._balance

    @property
    def transaction_history(self) -> list[Transaction]:
        # ? Should this be exposed as a read-only property or not?
        return self._transaction_history


def main() -> None:
    account1 = BankAccount(initial_balance=100)
    account2 = BankAccount(initial_balance=50)

    account1.transfer(account2, 50)

    print(account1.balance)


if __name__ == "__main__":
    main()
