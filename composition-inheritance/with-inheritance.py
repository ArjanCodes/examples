from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Employee(ABC):

    name: str
    id: int

    @abstractmethod
    def pay(self):
        pass


@dataclass
class HourlyEmployee(Employee):

    pay_rate: float
    hours_worked: int = 0
    employer_cost: float = 1000

    def pay(self):
        return self.pay_rate * self.hours_worked + self.employer_cost


@dataclass
class SalariedEmployee(Employee):

    monthly_salary: float
    percentage: float = 1

    def pay(self):
        return self.monthly_salary * self.percentage


@dataclass
class Freelancer(Employee):

    pay_rate: float
    hours_worked: int = 0
    vat_number: str = ""

    def pay(self):
        return self.pay_rate * self.hours_worked


@dataclass
class SalariedEmployeeWithCommission(SalariedEmployee):

    commission: float = 100
    contracts_landed: float = 0

    def pay(self):
        return super().pay() + self.commission * self.contracts_landed


@dataclass
class HourlyEmployeeWithCommission(HourlyEmployee):

    commission: float = 100
    contracts_landed: float = 0

    def pay(self):
        return super().pay() + self.commission * self.contracts_landed


@dataclass
class FreelancerWithCommission(Freelancer):

    commission: float = 100
    contracts_landed: float = 0

    def pay(self):
        return super().pay() + self.commission * self.contracts_landed


h = HourlyEmployee(name="Henry", id=12346, pay_rate=50, hours_worked=100)
print(f"{h.name} worked for {h.hours_worked} hours and earned ${h.pay()}.")

s = SalariedEmployeeWithCommission(name="Sarah", id=47832, monthly_salary=5000, contracts_landed=10)
print(f"{s.name} landed {s.contracts_landed} contracts and earned ${s.pay()}.")
