from dataclasses import dataclass


@dataclass(frozen=True)
class Transaction:
    id: str
    customer_id: str
    amount: float
    country: str


@dataclass(frozen=True)
class Customer:
    id: str
    country: str
    average_transaction: float


@dataclass(frozen=True)
class Features:
    country_mismatch: bool
    amount_ratio: float


@dataclass(frozen=True)
class RiskAssessment:
    score: float
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Decision:
    transaction_id: str
    requires_review: bool
    assessment: RiskAssessment


def extract_features(
    transaction: Transaction,
    customer: Customer,
) -> Features:
    ratio = (
        transaction.amount / customer.average_transaction
        if customer.average_transaction > 0
        else 0.0
    )

    return Features(
        country_mismatch=transaction.country != customer.country,
        amount_ratio=ratio,
    )


def assess_risk(features: Features) -> RiskAssessment:
    score = 0.0
    reasons: list[str] = []

    if features.country_mismatch:
        score += 0.3
        reasons.append("Country mismatch")

    if features.amount_ratio > 5:
        score += 0.5
        reasons.append("Unusually large transaction")

    return RiskAssessment(
        score=score,
        reasons=tuple(reasons),
    )


def make_decision(
    transaction_id: str,
    assessment: RiskAssessment,
) -> Decision:
    return Decision(
        transaction_id=transaction_id,
        requires_review=assessment.score > 0.7,
        assessment=assessment,
    )


def analyze(
    transaction: Transaction,
    customer: Customer,
) -> Decision:
    features = extract_features(transaction, customer)
    assessment = assess_risk(features)
    decision = make_decision(transaction.id, assessment)

    return decision


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

    decision = analyze(transaction, customer)

    print("Transaction:", transaction)
    print("Decision:", decision)


if __name__ == "__main__":
    main()
