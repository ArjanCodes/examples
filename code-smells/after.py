from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List


class Role(Enum):
    President = 1
    VicePresident = 2
    Manager = 3
    Lead = 4
    Worker = 5
    Intern = 6


@dataclass
class Employee(ABC):
    name: str
    role: Role
    holidays: int = 25

    @abstractmethod
    def pay(self):
        pass

    def take_a_holiday(self):
        if self.holidays < 1:
            raise ValueError("You don't have any holidays left. Now back to work, you!")
        self.holidays -= 1
        print("Have fun on your holiday. Don't forget to check your emails!")

    def payout_a_holiday(self):
        # fixed nr of holidays for paying out is 5
        if self.holidays < 5:
            raise ValueError(
                f"You don't have enough holidays left over for a payout. Remaining holidays: {self.holidays}."
            )
        self.holidays -= 5
        print(f"Paying out a holiday. Holidays left: {self.holidays}")


@dataclass
class HourlyEmployee(Employee):

    hourly_rate: float = 50
    hours_worked: int = 10

    def pay(self):
        print(f"Paying employee {self.name} a hourly rate of ${self.hourly_rate} for {self.hours_worked} hours.")


@dataclass
class SalariedEmployee(Employee):

    monthly_salary: float = 5000

    def pay(self):
        print(f"Paying employee {self.name} a monthly salary of ${self.monthly_salary}.")


def find_employee(employees: List[Employee], role: Role):
    return next((e for e in employees if e.role == role), None)


employees = [
    SalariedEmployee(name="Louis", role=Role.Manager),
    HourlyEmployee(name="Brenda", role=Role.President),
    HourlyEmployee(name="Tim", role=Role.Intern),
]

print(find_employee(employees, role=Role.VicePresident))
print(find_employee(employees, role=Role.Manager))
print(find_employee(employees, role=Role.Intern))
employees[0].pay()
employees[0].take_a_holiday()
