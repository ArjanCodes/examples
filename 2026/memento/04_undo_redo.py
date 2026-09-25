"""A complete Memento example with undo, redo, and a deliberate state boundary."""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class Step:
    name: str
    enabled: bool = True


@dataclass(frozen=True)
class WorkflowSnapshot:
    """Only the state that an editor should restore."""

    name: str
    steps: tuple[Step, ...]


class Snapshotable[T](Protocol):
    def snapshot(self) -> T: ...

    def restore(self, snapshot: T) -> None: ...


class History[T]:
    """Stores mementos without knowing what they contain."""

    def __init__(self) -> None:
        self._undo: list[T] = []
        self._redo: list[T] = []

    def save(self, obj: Snapshotable[T]) -> None:
        self._undo.append(obj.snapshot())
        self._redo.clear()

    def undo(self, obj: Snapshotable[T]) -> bool:
        if not self._undo:
            return False

        self._redo.append(obj.snapshot())
        obj.restore(self._undo.pop())
        return True

    def redo(self, obj: Snapshotable[T]) -> bool:
        if not self._redo:
            return False

        self._undo.append(obj.snapshot())
        obj.restore(self._redo.pop())
        return True


class Workflow:
    def __init__(self, name: str, steps: list[Step]) -> None:
        self._name = name
        self._steps = steps
        self.last_run_at: datetime | None = None
        self.execution_count = 0

    def rename(self, name: str) -> None:
        self._name = name

    def add_step(self, step: Step) -> None:
        self._steps.append(step)

    def move_step(self, step_name: str, position: int) -> None:
        index = next(i for i, step in enumerate(self._steps) if step.name == step_name)
        step = self._steps.pop(index)
        self._steps.insert(position, step)

    def run(self, now: datetime) -> None:
        self.last_run_at = now
        self.execution_count += 1

    def snapshot(self) -> WorkflowSnapshot:
        return WorkflowSnapshot(name=self._name, steps=tuple(self._steps))

    def restore(self, snapshot: WorkflowSnapshot) -> None:
        self._name = snapshot.name
        self._steps = list(snapshot.steps)

    def describe(self) -> str:
        steps = ", ".join(step.name for step in self._steps)
        return f"{self._name}: [{steps}], executions: {self.execution_count}"


def main() -> None:
    workflow = Workflow(
        "Invoice processing",
        [Step("validate_invoice"), Step("charge_card")],
    )
    history: History[WorkflowSnapshot] = History()

    workflow.run(datetime(2026, 9, 10, 9, 0))
    history.save(workflow)
    workflow.rename("Process customer invoice")
    workflow.add_step(Step("send_confirmation"))
    workflow.move_step("charge_card", position=2)
    print(f"Edited: {workflow.describe()}")

    assert history.undo(workflow)
    print(f"Undone: {workflow.describe()}")
    assert workflow.execution_count == 1  # Runtime state is not part of the memento.

    assert history.redo(workflow)
    print(f"Redone: {workflow.describe()}")


if __name__ == "__main__":
    main()
