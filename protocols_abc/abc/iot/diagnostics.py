from iot.device import Device


def collect_diagnostics(device: Device) -> None:
    print("Connecting to diagnostics server.")
    status = device.status_update()
    print(f"Sending status update [{status}] to server.")
