import tkinter as tk

from presenter import Presenter

TITLE = "To Do List"
DELETE_BTN_TXT = "Delete"


class TodoList(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(TITLE)
        self.geometry("500x300")

    def init_ui(self, presenter: Presenter) -> None:
        self.presenter = presenter
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
        self.my_entry.bind("<Return>", self.on_add_task)
        self.my_entry.pack(fill=tk.X)

        self.del_task_button = tk.Button(
            self.frame,
            text=DELETE_BTN_TXT,
            width=6,
            pady=5,
            state=tk.DISABLED,
            command=self.on_delete_task,
        )
        self.del_task_button.pack(side=tk.TOP, anchor=tk.NE)

    def on_add_task(self, event=None) -> None:
        self.presenter.handle_add_task(self.my_entry.get())
        self.my_entry.delete(0, "end")

    def on_delete_task(self) -> None:
        index = self.task_list.curselection()[0]
        self.presenter.handle_delete_task(index)

    def on_select_task(self, event=None) -> None:
        self.del_task_button.config(state=tk.NORMAL)

    def on_focus_out(self, event=None) -> None:
        self.task_list.selection_clear(0, tk.END)
        self.del_task_button.config(state=tk.DISABLED)

    def update_task_list(self, tasks: list[str]) -> None:
        self.task_list.delete(0, tk.END)
        for task in tasks:
            self.task_list.insert(tk.END, task)
        self.del_task_button.config(state=tk.DISABLED)
        self.task_list.yview(tk.END)
