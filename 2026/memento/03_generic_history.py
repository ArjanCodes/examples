"""Make the caretaker work with any object that supports snapshots."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Step:
    name: str
    enabled: bool = True


@dataclass(frozen=True)
class WorkflowSnapshot:
    name: str
    steps: tuple[Step, ...]


class Snapshotable[T](Protocol):
    def snapshot(self) -> T: ...

    def restore(self, snapshot: T) -> None: ...


class History[T]:
    def __init__(self) -> None:
        self._snapshots: list[T] = []

    def save(self, obj: Snapshotable[T]) -> None:
        self._snapshots.append(obj.snapshot())

    def undo(self, obj: Snapshotable[T]) -> bool:
        if not self._snapshots:
            return False

        obj.restore(self._snapshots.pop())
        return True


class Workflow:
    def __init__(self, name: str, steps: list[Step]) -> None:
        self._name = name
        self._steps = steps

    def rename(self, name: str) -> None:
        self._name = name

    def snapshot(self) -> WorkflowSnapshot:
        return WorkflowSnapshot(name=self._name, steps=tuple(self._steps))

    def restore(self, snapshot: WorkflowSnapshot) -> None:
        self._name = snapshot.name
        self._steps = list(snapshot.steps)

    def describe(self) -> str:
        return f"{self._name}: {[step.name for step in self._steps]}"


def main() -> None:
    workflow = Workflow("Invoice processing", [Step("charge_card")])
    history: History[WorkflowSnapshot] = History()

    history.save(workflow)
    workflow.rename("Process customer invoice")
    print(f"Edited: {workflow.describe()}")

    history.undo(workflow)
    print(f"Undone: {workflow.describe()}")


if __name__ == "__main__":
    main()
