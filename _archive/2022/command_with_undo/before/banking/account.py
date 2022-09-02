from dataclasses import dataclass


@dataclass
class Account:
    name: str
    number: str
    balance: int = 0

    def deposit(self, amount: int) -> None:
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
