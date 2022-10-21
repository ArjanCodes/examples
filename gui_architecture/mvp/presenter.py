from __future__ import annotations

from typing import Protocol

from model import Model


class View(Protocol):
    def init_ui(self, presenter: Presenter) -> None:
        ...

    def update_task_list(self, tasks: list[str]) -> None:
        ...

    def mainloop(self) -> None:
        ...


class Presenter:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.view.init_ui(self)
        self.view.update_task_list(self.model.get_tasks())

    def handle_add_task(self, task: str) -> None:
        self.model.add_task(task)
        self.view.update_task_list(self.model.get_tasks())

    def handle_delete_task(self, index: int) -> None:
        self.model.delete_task(index)
        self.view.update_task_list(self.model.get_tasks())

    def run(self) -> None:
        self.view.mainloop()
