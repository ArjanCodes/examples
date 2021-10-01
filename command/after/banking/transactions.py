from dataclasses import dataclass

from banking.account import Account
from banking.bank import Bank


@dataclass
class Deposit:
    account_number: str
    amount: int
    bank: Bank

    @property
    def account(self) -> Account:
        return self.bank.get_account(self.account_number)

    def execute(self) -> None:
        self.account.deposit(self.amount)
        print(f"Deposited ${self.amount}")

    def undo(self) -> None:
        self.account.withdraw(self.amount)
        print(f"Undid deposit of ${self.amount}")

    def redo(self) -> None:
        self.account.deposit(self.amount)
        print(f"Redid deposit of ${self.amount}")


@dataclass
class Withdrawal:
    account_number: str
    amount: int
    bank: Bank

    @property
    def account(self) -> Account:
        return self.bank.get_account(self.account_number)

    def execute(self) -> None:
        self.account.withdraw(self.amount)
        print(f"Withdrawn ${self.amount}")

    def undo(self) -> None:
        self.account.deposit(self.amount)
        print(f"Undid withdrawal of ${self.amount}")

    def redo(self) -> None:
        self.account.withdraw(self.amount)
        print(f"Redid withdrawal of ${self.amount}")


@dataclass
class Transfer:
    from_account_number: str
    to_account_number: str
    amount: int
    from_bank: Bank
    to_bank: Bank

    @property
    def from_account(self) -> Account:
        return self.from_bank.get_account(self.from_account_number)

    @property
    def to_account(self) -> Account:
        return self.to_bank.get_account(self.to_account_number)

    def execute(self) -> None:
        self.from_account.withdraw(self.amount)
        self.to_account.deposit(self.amount)
        print(f"Transferred ${self.amount}")

    def undo(self) -> None:
        self.to_account.withdraw(self.amount)
        self.from_account.deposit(self.amount)
        print(f"Undid transfer of ${self.amount}")

    def redo(self) -> None:
        self.from_account.withdraw(self.amount)
        self.to_account.deposit(self.amount)
        print(f"Redid transfer of ${self.amount}")
