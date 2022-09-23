import tkinter as tk
from functools import partial
from typing import Callable

from iot.devices import SmartSpeakerDevice
from iot.service import IOTService
from speaker_controller import send_msg_to_speaker

OFF_TEXT = "Speaker OFF"
ON_TEXT = "Speaker ON"


class SmartApp(tk.Tk):
    def __init__(self, toggle_speaker_fn: Callable[[str], None]) -> None:
        super().__init__()
        self.title("Smart App")
        self.geometry("400x250+300+300")
        self.speaker_on = False
        self.toggle_speaker_fn = toggle_speaker_fn

        self.create_ui()

    def create_ui(self) -> None:
        self.toggle_button = tk.Button(
            self, text=OFF_TEXT, width=10, command=self.toggle
        )
        self.toggle_button.pack(pady=10)

    def toggle(self) -> None:
        self.speaker_on = not self.speaker_on
        self.toggle_button.config(text=ON_TEXT if self.speaker_on else OFF_TEXT)

        self.toggle_speaker_fn("switch_on" if self.speaker_on else "switch_off")


def main():
    # create a IOT service
    service = IOTService()

    # create the smart speaker
    smart_speaker = SmartSpeakerDevice()
    speaker_id = service.register_device(smart_speaker)
    toggle_speaker_fn = partial(
        send_msg_to_speaker, service=service, speaker_id=speaker_id
    )

    app = SmartApp(toggle_speaker_fn)
    app.mainloop()


if __name__ == "__main__":
    main()
