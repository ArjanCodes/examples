from dataclasses import dataclass, field

from banking.transaction import Transaction


@dataclass
class BankController:
    undo_stack: list[Transaction] = field(default_factory=list)
    redo_stack: list[Transaction] = field(default_factory=list)

    def execute(self, transaction: Transaction):
        transaction.execute()
        self.redo_stack.clear()
        self.undo_stack.append(transaction)

    def undo(self):
        if len(self.undo_stack) == 0:
            return
        transaction = self.undo_stack.pop()
        transaction.undo()
        self.redo_stack.append(transaction)

    def redo(self):
        if len(self.redo_stack) == 0:
            return
        transaction = self.redo_stack.pop()
        transaction.execute()
        self.undo_stack.append(transaction)
