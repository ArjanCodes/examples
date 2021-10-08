from dataclasses import dataclass, field

from banking.transaction import Transaction


@dataclass
class BankController:
    ledger: list[Transaction] = field(default_factory=list)
    current: int = 0

    def execute(self, transaction: Transaction) -> None:
        del self.ledger[self.current :]
        self.ledger.append(transaction)
        self.current += 1

    def undo(self) -> None:
        if self.current > 0:
            self.current -= 1

    def redo(self) -> None:
        if self.current < len(self.ledger):
            self.current += 1

    def compute_balances(self) -> None:
        for transaction in self.ledger[: self.current]:
            transaction.execute()
