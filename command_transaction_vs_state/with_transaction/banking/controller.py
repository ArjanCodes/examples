from dataclasses import dataclass, field

from banking.transaction import Transaction


@dataclass
class BankController:
    stack: list[Transaction] = field(default_factory=list)
    current: int = 0

    def execute(self, transaction: Transaction) -> None:
        del self.stack[self.current :]
        self.stack.append(transaction)
        self.current += 1

    def undo(self) -> None:
        if self.current > 0:
            self.current -= 1

    def redo(self) -> None:
        if self.current < len(self.stack):
            self.current += 1

    def compute_balance_cache(self) -> None:
        for transaction in self.stack[: self.current]:
            transaction.execute()
