from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum, auto
from uuid import UUID, uuid4


class Feature(StrEnum):
    BASIC_ANALYTICS = auto()
    EXPORT_DATA = auto()
    CUSTOM_REPORTS = auto()
    SSO = auto()
    AUDIT_LOG = auto()


@dataclass
class Subscription:
    customer_id: UUID
    started_at: datetime

    monthly_price: Decimal = Decimal("0.00")
    max_projects: int = 0
    storage_gb: int = 0
    features: frozenset[Feature] = frozenset()

    def supports(self, feature: Feature) -> bool:
        return feature in self.features

    def can_create_project(self, current_projects: int) -> bool:
        return current_projects <= self.max_projects


class FreeSubscription(Subscription):
    def __init__(self, customer_id: UUID, started_at: datetime) -> None:
        super().__init__(
            customer_id=customer_id,
            started_at=started_at,
            monthly_price=Decimal("0.00"),
            max_projects=3,
            storage_gb=1,
            features=frozenset({Feature.BASIC_ANALYTICS}),
        )


class ProSubscription(Subscription):
    def __init__(self, customer_id: UUID, started_at: datetime) -> None:
        super().__init__(
            customer_id=customer_id,
            started_at=started_at,
            monthly_price=Decimal("20.00"),
            max_projects=50,
            storage_gb=100,
            features=frozenset(
                {Feature.BASIC_ANALYTICS, Feature.EXPORT_DATA, Feature.CUSTOM_REPORTS}
            ),
        )


class BusinessSubscription(Subscription):
    def __init__(self, customer_id: UUID, started_at: datetime) -> None:
        super().__init__(
            customer_id=customer_id,
            started_at=started_at,
            monthly_price=Decimal("75.00"),
            max_projects=250,
            storage_gb=1_000,
            features=frozenset(
                {
                    Feature.BASIC_ANALYTICS,
                    Feature.EXPORT_DATA,
                    Feature.CUSTOM_REPORTS,
                    Feature.SSO,
                    Feature.AUDIT_LOG,
                }
            ),
        )


def main() -> None:
    subscription = ProSubscription(
        customer_id=uuid4(),
        started_at=datetime.now(UTC),
    )

    print(f"{type(subscription).__name__}: ${subscription.monthly_price}/month")
    print(f"Can export data: {subscription.supports(Feature.EXPORT_DATA)}")
    print(f"Can use SSO: {subscription.supports(Feature.SSO)}")
    print(f"Can create project 50: {subscription.can_create_project(50)}")


if __name__ == "__main__":
    main()
