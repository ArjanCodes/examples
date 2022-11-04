import tkinter as tk
from pathlib import Path
from tkinter import filedialog

DEFAULT_FILENAME = "untitled.txt"


class WorsePad(tk.Tk):
    def __init__(self, show_save_button: bool = True) -> None:
        super().__init__()
        self.title("Worsepad")
        self.geometry("400x250+300+300")
        self.file_path = Path.cwd() / DEFAULT_FILENAME
        self.show_save_button = show_save_button
        self.create_ui()

    def create_ui(self) -> None:
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar)
        for label, command in (
            ("Open", self.on_open),
            ("Clear", self.on_clear),
            ("Save", self.on_save),
            ("Exit", self.quit),
        ):
            file_menu.add_command(label=label, command=command)

        menubar.add_cascade(label="File", menu=file_menu)

        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=1)

        if self.show_save_button:
            save_button = tk.Button(frame, text="Save", command=self.on_save)
            save_button.pack(anchor="e", padx=5, pady=5)

        self.text = tk.Text(frame)
        self.text.pack(fill=tk.BOTH, expand=1)

    def on_open(self) -> None:
        file_str = filedialog.askopenfilename(title="Select file")

        if not file_str:
            return

        self.file_path = Path(file_str)
        text_content = self.file_path.read_text(encoding="latin-1")

        self.on_clear()
        self.text.insert(tk.END, text_content)

    def on_clear(self) -> None:
        self.text.delete(1.0, tk.END)

    def on_save(self) -> None:
        self.file_path.write_text(self.text.get(1.0, tk.END), encoding="latin-1")
