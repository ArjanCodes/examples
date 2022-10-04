import logging
import tkinter as tk

from iot.devices import SmartSpeakerDevice
from iot.service import IOTService
from message.helper import Message as Msg
from network.connection import Connection

OFF_TEXT = "Speaker OFF"
ON_TEXT = "Speaker ON"
STATUS_UPDATE_TEXT = "Status Update"


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
        self.get_status_button = tk.Button(
            self, text=STATUS_UPDATE_TEXT, width=10, command=self.display_status
        )
        self.status_label = tk.Label(self, text="")
        self.toggle_button.pack()
        self.get_status_button.pack()
        self.status_label.pack()

    def toggle(self) -> None:
        logging.info(f"Toggle speaker {self.speaker_id} with status {self.speaker_on}")

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

        logging.info(f"Speaker {self.speaker_id} status: {self.speaker_on}")

    def display_status(self) -> None:
        logging.info(f"Display status for IOT devices.")
        status = ""
        for device_id, device in self.service.devices().items():
            status += f"{device_id}: {device.status_update()}"
        self.status_label.config(text=status)
        logging.info(f"Status: {status}")


def main():
    logging.basicConfig(level=logging.INFO)
    app = SmartApp()
    app.mainloop()


if __name__ == "__main__":
    main()
