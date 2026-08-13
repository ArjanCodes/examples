"""Plan variation modeled with an enum and external configuration mappings."""

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


class PlanType(StrEnum):
    FREE = auto()
    PRO = auto()
    BUSINESS = auto()


FEATURES_BY_PLAN: dict[PlanType, frozenset[Feature]] = {
    PlanType.FREE: frozenset({Feature.BASIC_ANALYTICS}),
    PlanType.PRO: frozenset(
        {Feature.BASIC_ANALYTICS, Feature.EXPORT_DATA, Feature.CUSTOM_REPORTS}
    ),
    PlanType.BUSINESS: frozenset(
        {
            Feature.BASIC_ANALYTICS,
            Feature.EXPORT_DATA,
            Feature.CUSTOM_REPORTS,
            Feature.SSO,
            Feature.AUDIT_LOG,
        }
    ),
}
MONTHLY_PRICE_BY_PLAN = {
    PlanType.FREE: Decimal("0.00"),
    PlanType.PRO: Decimal("20.00"),
    PlanType.BUSINESS: Decimal("75.00"),
}
MAX_PROJECTS_BY_PLAN = {PlanType.FREE: 3, PlanType.PRO: 50, PlanType.BUSINESS: 250}
STORAGE_GB_BY_PLAN = {PlanType.FREE: 1, PlanType.PRO: 100, PlanType.BUSINESS: 1_000}


@dataclass
class Subscription:
    customer_id: UUID
    plan_type: PlanType
    started_at: datetime

    def supports(self, feature: Feature) -> bool:
        return feature in FEATURES_BY_PLAN[self.plan_type]

    def can_create_project(self, current_projects: int) -> bool:
        return current_projects < MAX_PROJECTS_BY_PLAN[self.plan_type]


def main() -> None:
    subscription = Subscription(
        customer_id=uuid4(),
        plan_type=PlanType.PRO,
        started_at=datetime.now(timezone.utc),
    )

    print(f"{subscription.plan_type.value}: ${MONTHLY_PRICE_BY_PLAN[subscription.plan_type]}/month")
    print(f"Storage: {STORAGE_GB_BY_PLAN[subscription.plan_type]} GB")
    print(f"Can export data: {subscription.supports(Feature.EXPORT_DATA)}")
    print(f"Can use SSO: {subscription.supports(Feature.SSO)}")
    print(f"Can create project 50: {subscription.can_create_project(50)}")


if __name__ == "__main__":
    main()
