"""Plan variation modeled with a SubscriptionPlan Type Object."""

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum, auto
from uuid import UUID, uuid4


class Feature(StrEnum):
    BASIC_ANALYTICS = auto()
    EXPORT_DATA = auto()
    CUSTOM_REPORTS = auto()
    SSO = auto()
    AUDIT_LOG = auto()


@dataclass(frozen=True)
class SubscriptionPlan:
    name: str
    monthly_price: Decimal
    max_projects: int
    storage_gb: int
    features: frozenset[Feature]

    def supports(self, feature: Feature) -> bool:
        return feature in self.features

    def can_create_project(self, current_projects: int) -> bool:
        return current_projects < self.max_projects


FREE = SubscriptionPlan(
    name="free", monthly_price=Decimal("0.00"), max_projects=3, storage_gb=1,
    features=frozenset({Feature.BASIC_ANALYTICS}),
)
PRO = SubscriptionPlan(
    name="pro", monthly_price=Decimal("20.00"), max_projects=50, storage_gb=100,
    features=frozenset({Feature.BASIC_ANALYTICS, Feature.EXPORT_DATA, Feature.CUSTOM_REPORTS}),
)
BUSINESS = SubscriptionPlan(
    name="business", monthly_price=Decimal("75.00"), max_projects=250, storage_gb=1_000,
    features=frozenset({Feature.BASIC_ANALYTICS, Feature.EXPORT_DATA, Feature.CUSTOM_REPORTS, Feature.SSO, Feature.AUDIT_LOG}),
)


@dataclass
class Subscription:
    customer_id: UUID
    plan: SubscriptionPlan
    started_at: datetime


def main() -> None:
    subscription = Subscription(
        customer_id=uuid4(), plan=PRO, started_at=datetime.now(timezone.utc)
    )

    print(f"{subscription.plan.name}: ${subscription.plan.monthly_price}/month")
    print(f"Storage: {subscription.plan.storage_gb} GB")
    print(f"Can export data: {subscription.plan.supports(Feature.EXPORT_DATA)}")
    print(f"Can use SSO: {subscription.plan.supports(Feature.SSO)}")
    print(f"Can create project 50: {subscription.plan.can_create_project(50)}")


if __name__ == "__main__":
    main()
