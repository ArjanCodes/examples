from dataclasses import dataclass

from ..employee import Employee


@dataclass
class SalariedEmployee(Employee):
    monthly_salary: float = 5000
