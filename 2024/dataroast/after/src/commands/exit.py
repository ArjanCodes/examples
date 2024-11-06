from time import sleep

from commands.command_base import Command, CommandArgs
from controller.events import raise_event
from pydantic.dataclasses import dataclass


@dataclass
class ExitCommandArgs(CommandArgs): ...


class ExitCommand(Command):
    def execute(self, _: ExitCommandArgs):  # type: ignore
        for mark in [".", "..", "..."]:
            raise_event("exit", mark)
            sleep(0.5)
        quit()
