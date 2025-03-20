from dataclasses import dataclass

from ..employee import Employee


@dataclass
class HourlyEmployee(Employee):
    hourly_rate: float = 50
    amount: int = 10
