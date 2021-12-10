from iot.message import MessageType


class HueLightDevice:
    def connect(self) -> None:
        print("Connecting Hue Light.")
        print("Hue Light connected.")

    def disconnect(self) -> None:
        print("Disconnecting Hue Light.")
        print("Hue Light disconnected.")

    def send_message(self, message_type: MessageType, data: str = "") -> None:
        print(
            f"Hue Light handling message of type {message_type.name} with data [{data}]."
        )
        print("Hue Light received message.")


class SmartSpeakerDevice:
    def connect(self) -> None:
        print("Connecting to Smart Speaker.")
        print("Smart Speaker connected.")

    def disconnect(self) -> None:
        print("Disconnecting Smart Speaker.")
        print("Smart Speaker disconnected.")

    def send_message(self, message_type: MessageType, data: str = "") -> None:
        print(
            f"Smart Speaker handling message of type {message_type.name} with data [{data}]."
        )
        print("Smart Speaker received message.")


class SmartToiletDevice:
    def connect(self) -> None:
        print("Connecting to Smart Toilet.")
        print("Smart Toilet connected.")

    def disconnect(self) -> None:
        print("Disconnecting Smart Toilet.")
        print("Smart Toilet disconnected.")

    def send_message(self, message_type: MessageType, data: str = "") -> None:
        print(
            f"Smart Toilet handling message of type {message_type.name} with data [{data}]."
        )
        print("Smart Toilet received message.")
