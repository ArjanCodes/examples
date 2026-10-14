from dataclasses import dataclass
from typing import Protocol

# ============================================================
# Domain data
# ============================================================


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


# ============================================================
# Functional core
# ============================================================


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


def assess_risk(
    features: Features,
    model_prediction: float,
) -> RiskAssessment:
    score = 0.0
    reasons: list[str] = []

    if features.country_mismatch:
        score += 0.3
        reasons.append("Country mismatch")

    if features.amount_ratio > 5:
        score += 0.3
        reasons.append("Unusually large transaction")

    score += model_prediction * 0.4

    if model_prediction > 0.8:
        reasons.append("High model risk prediction")

    return RiskAssessment(
        score=min(score, 1.0),
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


# ============================================================
# Interfaces for external dependencies
# ============================================================


class TransactionRepository(Protocol):
    def get(self, transaction_id: str) -> Transaction: ...


class CustomerRepository(Protocol):
    def get(self, customer_id: str) -> Customer: ...


class DecisionRepository(Protocol):
    def save(self, decision: Decision) -> None: ...


class RiskModel(Protocol):
    def predict(self, features: Features) -> float: ...


class Notifier(Protocol):
    def send_alert(self, decision: Decision) -> None: ...


# ============================================================
# Implementations
# ============================================================


class InMemoryTransactionRepository:
    def __init__(self, transactions: list[Transaction]) -> None:
        self._transactions = {
            transaction.id: transaction for transaction in transactions
        }

    def get(self, transaction_id: str) -> Transaction:
        return self._transactions[transaction_id]


class InMemoryCustomerRepository:
    def __init__(self, customers: list[Customer]) -> None:
        self._customers = {customer.id: customer for customer in customers}

    def get(self, customer_id: str) -> Customer:
        return self._customers[customer_id]


class InMemoryDecisionRepository:
    def __init__(self) -> None:
        self.decisions: list[Decision] = []

    def save(self, decision: Decision) -> None:
        self.decisions.append(decision)
        print(f"Saved decision for {decision.transaction_id}")


class SimpleRiskModel:
    """A stand-in for a trained machine-learning model."""

    def predict(self, features: Features) -> float:
        score = 0.1

        if features.country_mismatch:
            score += 0.4

        if features.amount_ratio > 5:
            score += 0.5

        return min(score, 1.0)


class ConsoleNotifier:
    def send_alert(self, decision: Decision) -> None:
        print(
            f"ALERT: Transaction {decision.transaction_id} "
            f"requires review (score={decision.assessment.score:.2f})"
        )


# ============================================================
# Imperative shell
# ============================================================


class FraudDetectionService:
    def __init__(
        self,
        transactions: TransactionRepository,
        customers: CustomerRepository,
        decisions: DecisionRepository,
        model: RiskModel,
        notifier: Notifier,
    ) -> None:
        self.transactions = transactions
        self.customers = customers
        self.decisions = decisions
        self.model = model
        self.notifier = notifier

    def analyze(self, transaction_id: str) -> Decision:
        # Load external data.
        transaction = self.transactions.get(transaction_id)
        customer = self.customers.get(transaction.customer_id)

        # Calculate features.
        features = extract_features(transaction, customer)

        # Obtain a model prediction.
        prediction = self.model.predict(features)

        # Pure business logic.
        assessment = assess_risk(features, prediction)
        decision = make_decision(transaction.id, assessment)

        # Perform side effects.
        self.decisions.save(decision)

        if decision.requires_review:
            self.notifier.send_alert(decision)

        return decision


def main() -> None:
    transactions = InMemoryTransactionRepository(
        [
            Transaction(
                id="T001",
                customer_id="C001",
                amount=750.0,
                country="US",
            ),
            Transaction(
                id="T002",
                customer_id="C001",
                amount=50.0,
                country="NL",
            ),
        ]
    )

    customers = InMemoryCustomerRepository(
        [
            Customer(
                id="C001",
                country="NL",
                average_transaction=100.0,
            ),
        ]
    )

    decisions = InMemoryDecisionRepository()

    service = FraudDetectionService(
        transactions=transactions,
        customers=customers,
        decisions=decisions,
        model=SimpleRiskModel(),
        notifier=ConsoleNotifier(),
    )

    for transaction_id in ("T001", "T002"):
        decision = service.analyze(transaction_id)
        print(decision)
        print()


if __name__ == "__main__":
    main()
