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
class HourlyContract(Contract):

    pay_rate: float
    hours_worked: int = 0
    employer_cost: float = 1000

    def get_payment(self):
        return self.pay_rate * self.hours_worked + self.employer_cost


@dataclass
class SalariedContract(Contract):

    monthly_salary: float
    percentage: float = 1

    def get_payment(self):
        return self.monthly_salary * self.percentage


@dataclass
class FreelancerContract(Contract):

    pay_rate: float
    hours_worked: int = 0
    vat_number: str = ""

    def get_payment(self):
        return self.pay_rate * self.hours_worked


hc = HourlyContract(pay_rate=50, hours_worked=100)
h = Employee(name="Henry", id=12346, contract=hc)
print(f"{h.name} worked for {hc.hours_worked} hours and earned ${h.pay()}.")

sc = SalariedContract(monthly_salary=5000)
c = Commission(contracts_landed=10)
s = Employee(name="Sarah", id=47832, contract=sc, commission=c)
print(f"{s.name} landed {c.contracts_landed} contracts and earned ${s.pay()}.")
