import tkinter as tk
from typing import Callable

OFF_TEXT = "Speaker OFF"
ON_TEXT = "Speaker ON"
STATUS_UPDATE_TEXT = "Status Update"


class SmartApp(tk.Tk):
    def __init__(
        self, power_speaker_fn: Callable[[bool], None], get_status_fn: Callable[[], str]
    ) -> None:
        super().__init__()
        self.title("Smart App")
        self.geometry("400x250+300+300")
        self.speaker_on = False
        self.power_speaker_fn = power_speaker_fn
        self.get_status_fn = get_status_fn

        self.create_ui()

    def create_ui(self) -> None:
        self.toggle_button = tk.Button(
            self, text=OFF_TEXT, width=10, command=self.toggle
        )
        self.get_status_button = tk.Button(
            self, text=STATUS_UPDATE_TEXT, width=10, command=self.display_status
        )
        self.status_label = tk.Label(self, text="")
        self.toggle_button.pack()
        self.get_status_button.pack()
        self.status_label.pack()

    def toggle(self) -> None:
        self.speaker_on = not self.speaker_on
        self.toggle_button.config(text=ON_TEXT if self.speaker_on else OFF_TEXT)
        self.power_speaker_fn(self.speaker_on)

    def display_status(self) -> None:
        status = self.get_status_fn()
        self.status_label.config(text=status)
