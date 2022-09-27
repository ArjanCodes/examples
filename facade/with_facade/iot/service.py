import random
import string
from typing import Protocol


def generate_id(length: int = 8):
    return "".join(random.choices(string.ascii_uppercase, k=length))


class Device(Protocol):
    def connect(self) -> None:
        ...

    def disconnect(self) -> None:
        ...

    def connection_info(self) -> tuple[str, int]:
        ...


class IOTService:
    def __init__(self):
        self.devices: dict[str, Device] = {}

    def register_device(self, device: Device) -> str:
        device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    def unregister_device(self, device_id: str) -> None:
        self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]
