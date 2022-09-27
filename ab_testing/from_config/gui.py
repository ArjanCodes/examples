from pathlib import Path
from tkinter import BOTH, END, Button, Frame, Menu, Text, Tk, filedialog

DEFAULT_FILENAME = "untitled.txt"


class WorsePad(Frame):
    def __init__(self, show_save_button: bool = True) -> None:
        super().__init__(Tk())
        self.master.title("Worsepad")
        self.master.geometry("400x250+300+300")
        self.file_path = Path.cwd() / DEFAULT_FILENAME
        self.show_save_button = show_save_button
        self.create_ui()

    def create_ui(self) -> None:
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = Menu(menubar)
        file_menu.add_command(label="Open", command=self.on_open)
        file_menu.add_command(label="Clear", command=self.on_clear)
        file_menu.add_command(label="Save", command=self.on_save)
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        self.master.title("Worsepad")
        self.pack(fill=BOTH, expand=1)

        if self.show_save_button:
            self.save_button = Button(self, text="Save", command=self.on_save)
            self.save_button.pack(fill=BOTH, expand=1)

        self.text = Text(self)
        self.text.pack(fill=BOTH, expand=1)

    def on_open(self) -> None:
        file_str = filedialog.askopenfilename(title="Select file")

        if not file_str:
            return

        self.file_path = Path(file_str)
        text_content = self.file_path.read_text(encoding="latin-1")

        self.text.delete(1.0, END)
        self.text.insert(END, text_content)

    def on_clear(self) -> None:
        self.text.delete(1.0, END)

    def on_save(self) -> None:
        self.file_path.write_text(self.text.get(1.0, END), encoding="latin-1")
