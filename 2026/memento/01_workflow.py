"""The editable object we want to support undo for."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    name: str
    enabled: bool = True


class Workflow:
    def __init__(self, name: str, steps: list[Step]) -> None:
        self._name = name
        self._steps = steps

    def rename(self, name: str) -> None:
        self._name = name

    def add_step(self, step: Step) -> None:
        self._steps.append(step)

    def describe(self) -> str:
        return f"{self._name}: {[step.name for step in self._steps]}"


def main() -> None:
    workflow = Workflow("Invoice processing", [Step("charge_card")])
    workflow.rename("Process customer invoice")
    workflow.add_step(Step("send_confirmation"))
    print(workflow.describe())


if __name__ == "__main__":
    main()
