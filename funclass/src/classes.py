from __future__ import annotations

from datetime import datetime
from enum import Enum


class TransactionType(Enum):

    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"


Transaction = tuple[TransactionType, datetime, int]


class InsufficientBalanceError(Exception):
    pass


class BankAccount:
    def __init__(self, initial_balance: int = 0) -> None:
        self._balance: int = initial_balance
        self._transaction_history: list[Transaction] = []

    def deposit(self, amount: int) -> None:
        self._balance += amount
        self._transaction_history.append(
            (TransactionType.DEPOSIT, datetime.now(), amount)
        )

    def withdraw(self, amount: int) -> None:
        if self._sufficient_balance(amount):
            self._balance -= amount
            self._transaction_history.append(
                (TransactionType.WITHDRAWAL, datetime.now(), amount)
            )
        else:
            raise InsufficientBalanceError

    def transfer(self, other: BankAccount, amount: int) -> None:
        if self._sufficient_balance(amount):
            timestamp = datetime.now()
            self._balance -= amount
            other._balance += amount
            self._transaction_history.append(
                (TransactionType.TRANSFER, timestamp, amount)
            )
        else:
            raise InsufficientBalanceError

    def _sufficient_balance(self, amount: int) -> bool:
        return amount <= self._balance

    @property
    def balance(self) -> int:
        return self._balance

    @property
    def transaction_history(self) -> list[Transaction]:
        return self._transaction_history


def main() -> None:

    account1 = BankAccount(initial_balance=100)
    account2 = BankAccount(initial_balance=500)

    account1.withdraw(50)
    print(f"Account 1 balance after withdraw: ${account1.balance}")

    account2.deposit(400)
    print(f"Account 2 balance after deposit: ${account2.balance}")

    account1.transfer(account2, 50)
    print(f"Account 1 balance after transfer: ${account1.balance}")
    print(f"Account 2 balance after transfer: ${account2.balance}")

    print(f"Account 1 transaction history:\n{account1.transaction_history}")
    print(f"Account 2 transaction history:\n{account2.transaction_history}")


if __name__ == "__main__":
    main()
