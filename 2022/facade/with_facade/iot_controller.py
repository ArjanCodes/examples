import logging
from typing import Protocol


class IOTFacade(Protocol):
    def power_speaker(self, on: bool) -> None: ...

    def get_status(self) -> str: ...


def get_status(iot: IOTFacade) -> str:
    logging.info(f"Display status for IOT devices.")
    status = iot.get_status()
    logging.info(f"Status: {status}")
    return status


def power_speaker(on: bool, iot: IOTFacade) -> None:
    logging.info(f"Powering speaker: {on}.")
    iot.power_speaker(on)
    logging.info(f"Message sent to speaker.")
