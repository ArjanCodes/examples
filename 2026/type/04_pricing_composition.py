"""A Type Object can compose genuinely different pricing algorithms."""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum, auto
from typing import Protocol


class Feature(StrEnum):
    BASIC_ANALYTICS = auto()
    EXPORT_DATA = auto()
    CUSTOM_REPORTS = auto()
    SSO = auto()
    AUDIT_LOG = auto()


@dataclass(frozen=True)
class Usage:
    active_seats: int
    api_requests: int


class PricingModel(Protocol):
    def monthly_price(self, usage: Usage) -> Decimal: ...


@dataclass(frozen=True)
class FixedPricing:
    amount: Decimal

    def monthly_price(self, usage: Usage) -> Decimal:
        return self.amount


@dataclass(frozen=True)
class UsageBasedPricing:
    base_price: Decimal
    included_seats: int
    price_per_extra_seat: Decimal
    included_api_requests: int
    price_per_1_000_extra_requests: Decimal

    def monthly_price(self, usage: Usage) -> Decimal:
        extra_seats = max(usage.active_seats - self.included_seats, 0)
        extra_request_blocks = max(usage.api_requests - self.included_api_requests, 0) / 1_000
        return self.base_price + (extra_seats * self.price_per_extra_seat) + (
            Decimal(str(extra_request_blocks)) * self.price_per_1_000_extra_requests
        )


@dataclass(frozen=True)
class SubscriptionPlan:
    name: str
    max_projects: int
    features: frozenset[Feature]
    pricing: PricingModel

    def price_for(self, usage: Usage) -> Decimal:
        return self.pricing.monthly_price(usage)


PRO = SubscriptionPlan(
    name="pro", max_projects=50,
    features=frozenset({Feature.BASIC_ANALYTICS, Feature.EXPORT_DATA, Feature.CUSTOM_REPORTS}),
    pricing=FixedPricing(Decimal("20.00")),
)
ENTERPRISE = SubscriptionPlan(
    name="enterprise", max_projects=10_000,
    features=frozenset({Feature.BASIC_ANALYTICS, Feature.EXPORT_DATA, Feature.CUSTOM_REPORTS, Feature.SSO, Feature.AUDIT_LOG}),
    pricing=UsageBasedPricing(
        base_price=Decimal("500.00"), included_seats=25,
        price_per_extra_seat=Decimal("12.00"), included_api_requests=100_000,
        price_per_1_000_extra_requests=Decimal("0.50"),
    ),
)


def main() -> None:
    usage = Usage(active_seats=40, api_requests=125_000)
    print(f"{PRO.name}: ${PRO.price_for(usage):.2f}/month")
    print(f"{ENTERPRISE.name}: ${ENTERPRISE.price_for(usage):.2f}/month for {usage.active_seats} seats")


if __name__ == "__main__":
    main()
