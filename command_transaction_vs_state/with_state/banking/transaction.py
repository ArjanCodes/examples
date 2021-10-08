from typing import Protocol


class Transaction(Protocol):
    def execute(self) -> None:
        raise NotImplementedError()

    def undo(self) -> None:
        raise NotImplementedError()

    def redo(self) -> None:
        raise NotImplementedError()
