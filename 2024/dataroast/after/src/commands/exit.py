from time import sleep

from events import raise_event

from .model import Model


def exit_app(_: Model) -> None:
    for mark in [".", "..", "..."]:
        raise_event("exit", mark)
        sleep(0.5)
    quit()
