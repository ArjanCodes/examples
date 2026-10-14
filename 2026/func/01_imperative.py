from dataclasses import dataclass


@dataclass
class Transaction:
    id: str
    customer_id: str
    amount: float
    country: str
    risk_score: float = 0.0
    flagged: bool = False


@dataclass
class Customer:
    id: str
    country: str
    average_transaction: float


def normalize_amount(amount: float) -> float:
    return round(amount, 2)


def save_transaction(transaction: Transaction) -> None:
    print(f"Saving transaction {transaction.id}")


def send_alert(transaction: Transaction) -> None:
    print(f"ALERT: Transaction {transaction.id} flagged!")


def analyze(transaction: Transaction, customer: Customer) -> None:
    transaction.amount = normalize_amount(transaction.amount)

    if transaction.country != customer.country:
        transaction.risk_score += 0.3

    if transaction.amount > customer.average_transaction * 5:
        transaction.risk_score += 0.5

    if transaction.risk_score > 0.7:
        transaction.flagged = True

    save_transaction(transaction)

    if transaction.flagged:
        send_alert(transaction)


def main() -> None:
    customer = Customer(
        id="C001",
        country="NL",
        average_transaction=100.0,
    )

    transaction = Transaction(
        id="T001",
        customer_id="C001",
        amount=750.123,
        country="US",
    )

    print("Before:", transaction)

    analyze(transaction, customer)

    print("After:", transaction)


if __name__ == "__main__":
    main()
