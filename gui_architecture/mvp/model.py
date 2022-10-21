from dataclasses import dataclass, field


def init_task_list() -> list[str]:
    return [
        "Process email inbox",
        "Write blog post",
        "Prepare video scripts",
        "Tax accounting",
        "Prepare presentation",
        "Go to the gym",
    ]


@dataclass
class Model:
    task_list: list[str] = field(default_factory=init_task_list)

    def add_task(self, task: str) -> None:
        self.task_list.append(task)

    def delete_task(self, index: int) -> None:
        del self.task_list[index]

    def get_tasks(self) -> list[str]:
        return self.task_list.copy()
