from model import Model
from view import TodoList


class Controller:
    def __init__(self, model: Model, view: TodoList) -> None:
        self.model = model
        self.view = view
        self.view.bind_add_task(self.add_task)
        self.view.bind_delete_task(self.delete_task)

    def add_task(self, event=None) -> None:
        task = self.view.get_entry_text()
        self.view.clear_entry()
        self.model.add_task(task)
        self.view.update_task_list()

    def delete_task(self, event=None) -> None:
        self.model.delete_task(self.view.selected_task)
        self.view.update_task_list()

    def run(self) -> None:
        self.view.mainloop()
