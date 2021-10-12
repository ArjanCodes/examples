from typing import Protocol


class Device(Protocol):
    def status_update(self) -> str:
        ...


def collect_diagnostics(device: Device) -> None:
    print("Connecting to diagnostics server.")
    status = device.status_update()
    print(f"Sending status update [{status}] to server.")
