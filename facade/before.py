import tkinter as tk

from iot.devices import SmartSpeakerDevice
from iot.service import IOTService
from message.helper import Message as Msg
from network.connection import Connection

OFF_TEXT = "Speaker OFF"
ON_TEXT = "Speaker ON"


class SmartApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Smart App")
        self.geometry("400x250+300+300")
        self.speaker_on = False

        # create a IOT service
        self.service = IOTService()

        # create the smart speaker
        smart_speaker = SmartSpeakerDevice()
        self.speaker_id = self.service.register_device(smart_speaker)

        self.create_ui()

    def create_ui(self) -> None:
        self.toggle_button = tk.Button(
            self, text=OFF_TEXT, width=10, command=self.toggle
        )
        self.toggle_button.pack(pady=10)

    def toggle(self) -> None:
        self.speaker_on = not self.speaker_on
        self.toggle_button.config(text=ON_TEXT if self.speaker_on else OFF_TEXT)

        # create a connection to the smart speaker
        speaker_ip, speaker_port = self.service.get_device(
            self.speaker_id
        ).connection_info()
        speaker_connection = Connection(speaker_ip, speaker_port)

        # construct a message
        message = Msg(
            "SERVER", self.speaker_id, "switch_on" if self.speaker_on else "switch_off"
        )

        # send the message
        speaker_connection.connect()
        speaker_connection.send(message.b64)
        speaker_connection.disconnect()


def main():
    app = SmartApp()
    app.mainloop()


if __name__ == "__main__":
    main()
