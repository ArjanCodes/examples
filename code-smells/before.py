"""
Very advanced Employee management system.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Employee:
    """Basic representation of an employee at the company."""

    name: str
    role: str
    holidays: int = 25

    def take_a_holiday(self, payout: bool):
        """Let the employee take a single holiday, or pay out 5 holidays."""
        if payout:
            # fixed nr of holidays for paying out is 5
            if self.holidays < 5:
                raise ValueError(
                    f"You don't have enough holidays left over for a payout.\
                        Remaining holidays: {self.holidays}."
                )
            try:
                self.holidays -= 5
                print(f"Paying out a holiday. Holidays left: {self.holidays}")
            except Exception:
                # this should never happen
                pass
        else:
            if self.holidays < 1:
                raise ValueError("You don't have any holidays left. Now back to work, you!")
            self.holidays -= 1
            print("Have fun on your holiday. Don't forget to check your emails!")


@dataclass
class HourlyEmployee(Employee):
    """Employee that's paid based on number of worked hours."""

    hourly_rate: float = 50
    amount: int = 10


@dataclass
class SalariedEmployee(Employee):
    """Employee that's paid based on a fixed monthly salary."""

    monthly_salary: float = 5000


def find_manager(employees: List[Employee]):
    """Find a manager employee."""
    for employee in employees:
        if employee.role == "manager":
            return employee
    return None


def find_vice_president(employees: List[Employee]):
    """Find a vice-president employee."""
    for employee in employees:
        if employee.role == "vice_president":
            return employee
    return None


def find_intern(employees: List[Employee]):
    """Find an intern."""
    for employee in employees:
        if employee.role == "intern":
            return employee
    return None


def pay_employee(employee: Employee):
    """Pay an employee."""
    if isinstance(employee, SalariedEmployee):
        print(f"Paying employee {employee.name} a monthly salary of ${employee.monthly_salary}.")
    elif isinstance(employee, HourlyEmployee):
        print(
            f"Paying employee {employee.name} a hourly rate of \
            ${employee.hourly_rate} for {employee.amount} hours."
        )


my_employees = [
    SalariedEmployee(name="Louis", role="manager"),
    HourlyEmployee(name="Brenda", role="president"),
    HourlyEmployee(name="Tim", role="intern"),
]

print(find_vice_president(my_employees))
print(find_manager(my_employees))
print(find_intern(my_employees))
pay_employee(my_employees[0])
my_employees[0].take_a_holiday(False)
