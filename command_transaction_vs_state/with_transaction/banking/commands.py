from dataclasses import dataclass, field

from banking.account import Account
from banking.transaction import Transaction


@dataclass
class Deposit:
    account: Account
    amount: int

    @property
    def transfer_details(self) -> str:
        return f"${self.amount/100:.2f} to account {self.account.name}"

    def execute(self) -> None:
        self.account.deposit(self.amount)
        print(f"Deposited {self.transfer_details}")


@dataclass
class Withdrawal:
    account: Account
    amount: int

    @property
    def transfer_details(self) -> str:
        return f"${self.amount/100:.2f} from account {self.account.name}"

    def execute(self) -> None:
        self.account.withdraw(self.amount)
        print(f"Withdrawn {self.transfer_details}")


@dataclass
class Transfer:
    from_account: Account
    to_account: Account
    amount: int

    @property
    def transfer_details(self) -> str:
        return (
            f"${self.amount/100:.2f} from account {self.from_account.name}"
            f" to account {self.to_account.name}"
        )

    def execute(self) -> None:
        self.from_account.withdraw(self.amount)
        self.to_account.deposit(self.amount)
        print(f"Transferred {self.transfer_details}")


@dataclass
class Batch:
    commands: list[Transaction] = field(default_factory=list)

    def execute(self) -> None:
        completed_commands: list[Transaction] = []
        try:
            for command in self.commands:
                command.execute()
                completed_commands.append(command)
        except ValueError:
            for command in reversed(completed_commands):
                command.undo()
            raise
