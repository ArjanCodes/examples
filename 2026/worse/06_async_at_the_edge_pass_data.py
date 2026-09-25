import asyncio
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


@dataclass(frozen=True)
class Order:
    id: int
    customer_id: int
    total_cents: int


@dataclass(frozen=True)
class CreditProfile:
    available_credit_cents: int
    overdue_balance_cents: int
    fraud_score: int
    account_age_days: int


class Decision(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"
    MANUAL_REVIEW = "manual review"


@dataclass(frozen=True)
class CheckoutDecision:
    decision: Decision
    reason: str


class CreditProfileProvider(Protocol):
    """Synchronous port used by the domain policy."""

    def get_profile(self, customer_id: int) -> CreditProfile: ...


class CheckoutPolicy:
    def decide_checkout(self, order: Order, profile: CreditProfile) -> CheckoutDecision:
        """The domain can retrieve data without becoming async itself."""
        if profile.fraud_score >= 80:
            return CheckoutDecision(Decision.MANUAL_REVIEW, "High fraud score")
        if profile.overdue_balance_cents > 0:
            return CheckoutDecision(Decision.REJECTED, "Customer has overdue invoices")
        if order.total_cents > profile.available_credit_cents:
            return CheckoutDecision(Decision.REJECTED, "Insufficient available credit")
        if order.total_cents > 50_000 and profile.account_age_days < 30:
            return CheckoutDecision(
                Decision.MANUAL_REVIEW, "New account with a large order"
            )
        return CheckoutDecision(Decision.APPROVED, "Credit policy passed")


class AsyncCreditApi:
    async def fetch_profile(self, customer_id: int) -> CreditProfile:
        """Pretend this is an async HTTP client."""
        await asyncio.sleep(0.01)
        print(f"Fetched credit profile for customer {customer_id}")
        return CreditProfile(
            available_credit_cents=12_000,
            overdue_balance_cents=0,
            fraud_score=12,
            account_age_days=120,
        )


async def main() -> None:
    policy = CheckoutPolicy()
    credit_profile_provider = AsyncCreditApi()
    order = Order(id=42, customer_id=7, total_cents=8_000)
    profile = await credit_profile_provider.fetch_profile(order.customer_id)
    decision = policy.decide_checkout(order, profile)
    print(f"Order {order.id}: {decision.decision} ({decision.reason})")


if __name__ == "__main__":
    asyncio.run(main())
