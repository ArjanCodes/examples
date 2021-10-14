from typing import Protocol


class DiagnosticsSource(Protocol):
    def status_update(self) -> str:
        ...


def collect_diagnostics(device: DiagnosticsSource) -> None:
    print("Connecting to diagnostics server.")
    status = device.status_update()
    print(f"Sending status update [{status}] to server.")
