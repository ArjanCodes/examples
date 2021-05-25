"""Very advanced Employee management system"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List


class Role(Enum):
    """Employee roles"""

    PRESIDENT = 1
    VICEPRESIDENT = 2
    MANAGER = 3
    LEAD = 4
    WORKER = 5
    INTERN = 6


@dataclass
class Employee(ABC):
    """Basic representation of an employee at the company."""

    name: str
    role: Role
    holidays: int = 25

    @abstractmethod
    def pay(self):
        """Method to call when paying an employee"""

    def take_a_holiday(self):
        """Let the employee take a holiday (lazy bastard)"""
        if self.holidays < 1:
            raise ValueError("You don't have any holidays left. Now back to work, you!")
        self.holidays -= 1
        print("Have fun on your holiday. Don't forget to check your emails!")

    def payout_a_holiday(self):
        """Let the employee get paid for unused holidays."""
        # fixed nr of holidays for paying out is 5
        if self.holidays < 5:
            raise ValueError(
                f"You don't have enough holidays left over for a payout.\
                    Remaining holidays: {self.holidays}."
            )
        self.holidays -= 5
        print(f"Paying out a holiday. Holidays left: {self.holidays}")


@dataclass
class HourlyEmployee(Employee):
    """Employee that's paid based on number of worked hours."""

    hourly_rate: float = 50
    hours_worked: int = 10

    def pay(self):
        print(
            f"Paying employee {self.name} a hourly rate of \
            ${self.hourly_rate} for {self.hours_worked} hours."
        )


@dataclass
class SalariedEmployee(Employee):
    """Employee that's paid based on a fixed monthly salary."""

    monthly_salary: float = 5000

    def pay(self):
        print(f"Paying employee {self.name} a monthly salary of ${self.monthly_salary}.")


def find_employee(employees: List[Employee], role: Role):
    """Find an employee with a particular role in the employee list"""
    return next((e for e in employees if e.role == role), None)


my_employees = [
    SalariedEmployee(name="Louis", role=Role.MANAGER),
    HourlyEmployee(name="Brenda", role=Role.PRESIDENT),
    HourlyEmployee(name="Tim", role=Role.INTERN),
]

print(find_employee(my_employees, role=Role.VICEPRESIDENT))
print(find_employee(my_employees, role=Role.MANAGER))
print(find_employee(my_employees, role=Role.INTERN))
my_employees[0].pay()
my_employees[0].take_a_holiday()
