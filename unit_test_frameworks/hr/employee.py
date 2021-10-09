"""
Very advanced Employee management system.
"""
from dataclasses import dataclass, field
from typing import Optional, Protocol


class PaymentSource(Protocol):
    def compute_pay(self) -> int:
        ...


@dataclass
class DealBasedCommission:

    commission: int = 10000
    deals_landed: int = 0

    def compute_pay(self) -> int:
        return self.commission * self.deals_landed


@dataclass
class HourlyContract:

    hourly_rate: int
    hours_worked: float = 0.0
    employer_cost: int = 100000

    def compute_pay(self) -> int:
        return int(self.hourly_rate * self.hours_worked + self.employer_cost)


@dataclass
class Employee:

    name: str
    id: int
    payment_sources: list[PaymentSource] = field(default_factory=list)

    def add_payment_source(self, payment_source: PaymentSource):
        self.payment_sources.append(payment_source)

    def compute_pay(self) -> int:
        return sum(source.compute_pay() for source in self.payment_sources)
