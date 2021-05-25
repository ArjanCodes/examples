from dataclasses import dataclass
from typing import List


@dataclass
class Employee:
    name: str
    role: str
    holidays: int = 25

    def take_a_holiday(self, payout: bool):
        if payout:
            # fixed nr of holidays for paying out is 5
            if self.holidays < 5:
                raise ValueError(
                    f"You don't have enough holidays left over for a payout. Remaining holidays: {self.holidays}."
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

    hourly_rate: float = 50
    amount: int = 10


@dataclass
class SalariedEmployee(Employee):

    monthly_salary: float = 5000


def find_manager(employees: List[Employee]):
    for e in employees:
        if e.role == "manager":
            return e
    return None


def find_vice_president(employees: List[Employee]):
    for e in employees:
        if e.role == "vice_president":
            return e
    return None


def find_intern(employees: List[Employee]):
    for e in employees:
        if e.role == "intern":
            return e
    return None


def pay_employee(e: Employee):
    if isinstance(e, SalariedEmployee):
        print(f"Paying employee {e.name} a monthly salary of ${e.monthly_salary}.")
    elif isinstance(e, HourlyEmployee):
        print(f"Paying employee {e.name} a hourly rate of ${e.hourly_rate} for {e.amount} hours.")


employees = [
    SalariedEmployee(name="Louis", role="manager"),
    HourlyEmployee(name="Brenda", role="president"),
    HourlyEmployee(name="Tim", role="intern"),
]

print(find_vice_president(employees))
print(find_manager(employees))
print(find_intern(employees))
pay_employee(employees[0])
employees[0].take_a_holiday(False)
