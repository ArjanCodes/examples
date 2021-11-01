from typing import Protocol


class Transaction(Protocol):
    def execute(self) -> None:
        ...
