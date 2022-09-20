from pathlib import Path
from tkinter import BOTH, END, Frame, Menu, Text, Tk, filedialog
from tkinter.messagebox import showwarning


class WorsePad(Frame):
    def __init__(self, master: Tk) -> None:
        super().__init__(master)
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

        self.text = Text(self)
        self.text.pack(fill=BOTH, expand=1)

    def on_open(self) -> None:
        file_str = filedialog.askopenfilename(title="Select file")

        if not file_str:
            return

        file_path = Path(file_str)
        text_content = file_path.read_text(encoding="latin-1")
        print(text_content)

        self.text.delete(1.0, END)
        self.text.insert(END, text_content)

    def on_clear(self) -> None:
        self.text.delete(1.0, END)

    def on_save(self) -> None:
        showwarning("Saving", "To do.")


def main():
    root = Tk()
    root.title("Worsepad")
    root.geometry("400x250+300+300")
    _ = WorsePad(root)
    root.mainloop()


if __name__ == "__main__":
    main()
