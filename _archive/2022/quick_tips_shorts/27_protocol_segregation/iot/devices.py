from iot.message import MessageType


class SmartBattery:
    def check_status(self) -> None:
        print("Battery online.")


class HueLight:
    def check_status(self) -> None:
        print("Hue Light connected.")

    def send_message(self, message_type: MessageType, data: str = "") -> None:
        print(
            f"Hue Light handling message of type {message_type.name} with data [{data}]."
        )
        print("Hue Light received message.")


class SmartSpeaker:
    def check_status(self) -> None:
        print("Smart Speaker connected.")

    def send_message(self, message_type: MessageType, data: str = "") -> None:
        print(
            f"Smart Speaker handling message of type {message_type.name} with data [{data}]."
        )
        print("Smart Speaker received message.")
