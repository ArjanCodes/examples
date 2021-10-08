"""
Very advanced Employee management system.
"""
from dataclasses import dataclass


@dataclass
class Employee:
    """Basic representation of an employee."""

    name: str
    employee_id: int
    pay_rate: int = 10000
    hours_worked: float = 0.0
    employer_cost: int = 100000
    commission: int = 10000
    contracts_landed: int = 0

    @property
    def has_commission(self) -> bool:
        """Whether the employee has a commission."""
        return self.commission > 0

    def compute_payout(self) -> int:
        """Compute how much the employee should be paid."""
        if self.hours_worked < 0:
            raise ValueError(
                f"hours_worked should be a positive number, but got: {self.hours_worked}"
            )
        payout = self.pay_rate * self.hours_worked + self.employer_cost
        if self.has_commission:
            payout += self.commission * self.contracts_landed
        return int(payout)
