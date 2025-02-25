from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto
from typing import Protocol


class TransactionType(StrEnum):
    DEPOSIT = auto()
    WITHDRAWAL = auto()
    INTEREST = auto()


@dataclass
class Transaction:
    transaction_id: int
    transaction_type: TransactionType
    amount: int
    timestamp: datetime
    customer_id: int


class LoggableTransaction(Protocol):
    transaction_id: int
    transaction_type: TransactionType
    timestamp: datetime


def log_transaction(transaction: LoggableTransaction) -> None:
    print(
        f"Logging {transaction.transaction_type} transaction ID {transaction.transaction_id} at {transaction.timestamp}"
    )


def process_transaction(transaction_type: TransactionType, amount: int) -> None:
    if transaction_type == TransactionType.DEPOSIT:
        print(f"Processing deposit of {amount}")
    elif transaction_type == TransactionType.WITHDRAWAL:
        print(f"Processing withdrawal of {amount}")


def main() -> None:
    transaction = Transaction(
        transaction_id=123,
        transaction_type=TransactionType.DEPOSIT,
        amount=1000,
        timestamp=datetime.now(),
        customer_id=456,
    )

    log_transaction(transaction)
    process_transaction(transaction.transaction_type, transaction.amount)


if __name__ == "__main__":
    main()
