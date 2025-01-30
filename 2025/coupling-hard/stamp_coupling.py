from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto


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


def log_transaction(transaction: Transaction):
    print(
        f"Logging {transaction.transaction_type} transaction ID {transaction.transaction_id} at {transaction.timestamp}"
    )


def process_transaction(transaction: Transaction):
    if transaction.transaction_type == TransactionType.DEPOSIT:
        print(f"Processing deposit of {transaction.amount}")
    elif transaction.transaction_type == TransactionType.WITHDRAWAL:
        print(f"Processing withdrawal of {transaction.amount}")


def main() -> None:
    transaction = Transaction(
        transaction_id=123,
        transaction_type=TransactionType.DEPOSIT,
        amount=1000,
        timestamp=datetime.now(),
        customer_id=456,
    )

    log_transaction(transaction)
    process_transaction(transaction)


if __name__ == "__main__":
    main()
