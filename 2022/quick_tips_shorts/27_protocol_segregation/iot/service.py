from typing import Protocol

from iot.message import Message, MessageType


class Device(Protocol):
    def check_status(self) -> None: ...

    def send_message(self, message_type: MessageType, data: str) -> None: ...


class IOTService:
    def __init__(self):
        self.devices: dict[str, Device] = {}

    def register_device(self, device_id: str, device: Device):
        self.devices[device_id] = device

    def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]

    def run_program(self, program: list[Message]) -> None:
        print("=====RUNNING PROGRAM======")
        for msg in program:
            self.send_msg(msg)
        print("=====END OF PROGRAM======")

    def send_msg(self, msg: Message) -> None:
        self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
