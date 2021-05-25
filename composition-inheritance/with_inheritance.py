"""
Very advanced Employee management system.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Employee(ABC):
    """Basic representation of an employee at the company."""

    name: str
    id: int

    @abstractmethod
    def pay(self):
        """Pay an employee."""


@dataclass
class HourlyEmployee(Employee):
    """Employee that's paid based on number of worked hours."""

    pay_rate: float
    hours_worked: int = 0
    employer_cost: float = 1000

    def pay(self):
        return self.pay_rate * self.hours_worked + self.employer_cost


@dataclass
class SalariedEmployee(Employee):
    """Employee that's paid based on a fixed monthly salary."""

    monthly_salary: float
    percentage: float = 1

    def pay(self):
        return self.monthly_salary * self.percentage


@dataclass
class Freelancer(Employee):
    """Freelancer that's paid based on number of worked hours."""

    pay_rate: float
    hours_worked: int = 0
    vat_number: str = ""

    def pay(self):
        return self.pay_rate * self.hours_worked


@dataclass
class SalariedEmployeeWithCommission(SalariedEmployee):
    """Employee that's paid based on a fixed monthly salary and that gets a commission."""

    commission: float = 100
    contracts_landed: float = 0

    def pay(self):
        return super().pay() + self.commission * self.contracts_landed


@dataclass
class HourlyEmployeeWithCommission(HourlyEmployee):
    """Employee that's paid based on number of worked hours and that gets a commission."""

    commission: float = 100
    contracts_landed: float = 0

    def pay(self):
        return super().pay() + self.commission * self.contracts_landed


@dataclass
class FreelancerWithCommission(Freelancer):
    """Freelancer that's paid based on number of worked hours and that gets a commission."""

    commission: float = 100
    contracts_landed: float = 0

    def pay(self):
        return super().pay() + self.commission * self.contracts_landed


h = HourlyEmployee(name="Henry", id=12346, pay_rate=50, hours_worked=100)
print(f"{h.name} worked for {h.hours_worked} hours and earned ${h.pay()}.")

s = SalariedEmployeeWithCommission(
    name="Sarah", id=47832, monthly_salary=5000, contracts_landed=10
)
print(f"{s.name} landed {s.contracts_landed} contracts and earned ${s.pay()}.")
