from abc import ABC, abstractmethod
from dataclasses import dataclass


class Contract(ABC):

    @abstractmethod
    def get_payment(self):
        pass

@dataclass
class Commission:

    commission: float = 100
    contracts_landed: float = 0

    def get_payment(self):
        return self.commission * self.contracts_landed


@dataclass
class Employee:

    name: str
    id: int
    contract: Contract
    commission: Commission = None

    def pay(self):
        payout = self.contract.get_payment()
        if self.commission is not None:
            payout += self.commission.get_payment()
        return payout

@dataclass
class HourlyContract(ABC):

    pay_rate: float
    hours_worked: int = 0

    def get_payment(self):
        return self.pay_rate * self.hours_worked

@dataclass
class SalariedContract(ABC):

    monthly_salary: float
    percentage: float = 1

    def get_payment(self):
        return self.monthly_salary * self.percentage




hc = HourlyContract(50, 100)
h = Employee("Henry", 12346, hc)
print(f"{h.name} worked for {hc.hours_worked} hours and earned ${h.pay()}.")

sc = SalariedContract(5000)
c = Commission(contracts_landed=10)
s = Employee("Sarah", 47832, sc, c)
print(f"{s.name} landed {c.contracts_landed} contracts and earned ${s.pay()}.")
