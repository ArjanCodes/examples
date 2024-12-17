from src.commands.command_base import CommandArgs, Command
from src.controller.events import raise_event

from time import sleep
from pydantic.dataclasses import dataclass


@dataclass
class ExitCommandArgs(CommandArgs): ...


class ExitCommand(Command):
    def execute(self, _: ExitCommandArgs):  # type: ignore
        for mark in [".", "..", "..."]:
            raise_event("exit", mark)
            sleep(0.5)
        quit()
