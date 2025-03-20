from ..employees.employee import Employee
from ..employees.types.hourly import HourlyEmployee
from ..employees.types.salaried import SalariedEmployee


class Company:
    """Represents a company with employees."""

    def __init__(self) -> None:
        self.employees: list[Employee] = []

    def add_employee(self, employee: Employee) -> None:
        self.employees.append(employee)

    def find_managers(self) -> list[Employee]:
        return [e for e in self.employees if e.role == "manager"]

    def find_vice_presidents(self) -> list[Employee]:
        return [e for e in self.employees if e.role == "vice-president"]

    def find_support_staff(self) -> list[Employee]:
        return [e for e in self.employees if e.role == "support"]

    def pay_employee(self, employee: Employee) -> None:
        if isinstance(employee, SalariedEmployee):
            print(
                f"Paying employee {employee.name} a monthly salary of ${employee.monthly_salary}."
            )
        elif isinstance(employee, HourlyEmployee):
            print(
                f"Paying employee {employee.name} a hourly rate of \
                ${employee.hourly_rate} for {employee.amount} hours."
            )
