"""Let the workflow capture and restore its editable state."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    name: str
    enabled: bool = True


@dataclass(frozen=True)
class WorkflowSnapshot:
    name: str
    steps: tuple[Step, ...]


class Workflow:
    def __init__(self, name: str, steps: list[Step]) -> None:
        self._name = name
        self._steps = steps

    def rename(self, name: str) -> None:
        self._name = name

    def add_step(self, step: Step) -> None:
        self._steps.append(step)

    def snapshot(self) -> WorkflowSnapshot:
        return WorkflowSnapshot(name=self._name, steps=tuple(self._steps))

    def restore(self, snapshot: WorkflowSnapshot) -> None:
        self._name = snapshot.name
        self._steps = list(snapshot.steps)

    def describe(self) -> str:
        return f"{self._name}: {[step.name for step in self._steps]}"


def main() -> None:
    workflow = Workflow("Invoice processing", [Step("charge_card")])
    before_editing = workflow.snapshot()

    workflow.rename("Process customer invoice")
    workflow.add_step(Step("send_confirmation"))
    print(f"Edited: {workflow.describe()}")

    workflow.restore(before_editing)
    print(f"Restored: {workflow.describe()}")


if __name__ == "__main__":
    main()
