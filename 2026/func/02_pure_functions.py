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


def country_risk(
    transaction: Transaction,
    customer: Customer,
) -> float:
    return 0.3 if transaction.country != customer.country else 0.0


def amount_risk(
    transaction: Transaction,
    customer: Customer,
) -> float:
    if customer.average_transaction <= 0:
        return 0.0

    ratio = transaction.amount / customer.average_transaction

    return 0.5 if ratio > 5 else 0.0


def calculate_risk(
    transaction: Transaction,
    customer: Customer,
) -> float:
    return country_risk(transaction, customer) + amount_risk(transaction, customer)


def should_flag(score: float) -> bool:
    return score > 0.7


def save_transaction(transaction: Transaction) -> None:
    print(f"Saving transaction {transaction.id}")


def send_alert(transaction: Transaction) -> None:
    print(f"ALERT: Transaction {transaction.id} flagged!")


def analyze(transaction: Transaction, customer: Customer) -> None:
    transaction.risk_score = calculate_risk(transaction, customer)
    transaction.flagged = should_flag(transaction.risk_score)

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
        amount=750.0,
        country="US",
    )

    analyze(transaction, customer)

    print(transaction)

    # The calculations are independent of analyze().
    print("Country risk:", country_risk(transaction, customer))
    print("Amount risk:", amount_risk(transaction, customer))
    print("Total risk:", calculate_risk(transaction, customer))

    # Repeating the calculation gives the same result.
    print("Again:", calculate_risk(transaction, customer))


if __name__ == "__main__":
    main()
