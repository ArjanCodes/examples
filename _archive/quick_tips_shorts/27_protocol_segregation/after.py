from typing import Protocol

from iot.devices import HueLight, SmartBattery, SmartSpeaker
from iot.message import Message, MessageType


class Device(Protocol):
    def send_message(self, message_type: MessageType, data: str) -> None:
        ...


class StatusSource(Protocol):
    def check_status(self) -> None:
        ...


def run_program(program: list[Message], devices: dict[str, Device]) -> None:
    print("=====RUNNING PROGRAM======")
    for msg in program:
        devices[msg.device_id].send_message(msg.msg_type, msg.data)
    print("=====END OF PROGRAM======")


def check_status(devices: dict[str, StatusSource]) -> None:
    for device in devices.values():
        device.check_status()


def main() -> None:
    devices = {
        "hue_light": HueLight(),
        "speaker": SmartSpeaker(),
    }
    status_sources = devices | {
        "battery": SmartBattery(),
    }

    wake_up_program = [
        Message("hue_light", MessageType.SWITCH_ON),
        Message("speaker", MessageType.SWITCH_ON),
        Message("speaker", MessageType.PLAY_SONG, "Miles Davis - Kind of Blue"),
    ]

    # run the program
    run_program(wake_up_program, devices)

    # check the status
    check_status(status_sources)


if __name__ == "__main__":
    main()
