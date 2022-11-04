import tkinter as tk
from typing import Any, Callable

from model import Model

TITLE = "To Do List"
DELETE_BTN_TXT = "Delete"


class TodoList(tk.Tk):
    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model
        self.title(TITLE)
        self.geometry("500x300")
        self.create_ui()
        self.update_task_list()

    def create_ui(self) -> None:
        self.frame = tk.Frame(self, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.task_list = tk.Listbox(
            self.frame,
            height=10,
            activestyle="none",
        )
        self.task_list.bind("<FocusOut>", self.on_focus_out)
        self.task_list.bind("<<ListboxSelect>>", self.on_select_task)
        self.task_list.pack(fill=tk.X)

        self.my_entry = tk.Entry(self.frame)
        self.my_entry.pack(fill=tk.X)

        self.del_task_button = tk.Button(
            self.frame,
            text=DELETE_BTN_TXT,
            width=6,
            pady=5,
            state=tk.DISABLED,
        )
        self.del_task_button.pack(side=tk.TOP, anchor=tk.NE)

    def bind_delete_task(self, callback: Callable[[tk.Event], None]) -> None:
        self.del_task_button.bind("<Button-1>", callback)

    def bind_add_task(self, callback: Callable[[tk.Event], None]) -> None:
        self.my_entry.bind("<Return>", callback)

    def get_entry_text(self) -> str:
        return self.my_entry.get()

    def clear_entry(self) -> None:
        self.my_entry.delete(0, "end")

    @property
    def selected_task(self) -> str:
        return self.task_list.get(self.task_list.curselection())

    def on_select_task(self, event=None) -> None:
        self.del_task_button.config(state=tk.NORMAL)

    def on_focus_out(self, event=None) -> None:
        self.task_list.selection_clear(0, tk.END)
        self.del_task_button.config(state=tk.DISABLED)

    def update_task_list(self) -> None:
        self.task_list.delete(0, tk.END)
        for item in self.model.get_tasks():
            self.task_list.insert(tk.END, item)
        self.del_task_button.config(state=tk.DISABLED)
        self.task_list.yview(tk.END)
