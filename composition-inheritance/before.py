"""
Very advanced Employee management system.
"""

from dataclasses import dataclass


@dataclass
class HourlyEmployee:
    """Employee that's paid based on number of worked hours."""

    name: str
    id: int
    commission: float = 100
    contracts_landed: float = 0
    pay_rate: float = 0
    hours_worked: int = 0
    employer_cost: float = 1000

    def pay(self):
        """Pay an employee"""
        return (
            self.pay_rate * self.hours_worked
            + self.employer_cost
            + self.commission * self.contracts_landed
        )


@dataclass
class SalariedEmployee:
    """Employee that's paid based on a fixed monthly salary."""

    name: str
    id: int
    commission: float = 100
    contracts_landed: float = 0
    monthly_salary: float = 0
    percentage: float = 1

    def pay(self):
        """Pay an employee"""
        return self.monthly_salary * self.percentage + self.commission * self.contracts_landed


@dataclass
class Freelancer:
    """Freelancer that's paid based on number of worked hours."""

    name: str
    id: int
    commission: float = 100
    contracts_landed: float = 0
    pay_rate: float = 0
    hours_worked: int = 0
    vat_number: str = ""

    def pay(self):
        """Pay an employee"""
        return self.pay_rate * self.hours_worked + self.commission * self.contracts_landed


h = HourlyEmployee(name="Henry", id=12346, pay_rate=50, hours_worked=100)
print(f"{h.name} worked for {h.hours_worked} hours and earned ${h.pay()}.")

s = SalariedEmployee(name="Sarah", id=47832, monthly_salary=5000, contracts_landed=10)
print(f"{s.name} landed {s.contracts_landed} contracts and earned ${s.pay()}.")
