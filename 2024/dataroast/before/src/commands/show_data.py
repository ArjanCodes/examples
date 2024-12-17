from src.commands.validations import value_exists_in_dataframes
from src.commands.command_base import CommandArgs, Command
from src.controller.events import raise_event

from pydantic.dataclasses import dataclass
from pydantic import model_validator
from sys import maxsize


@dataclass
class ShowDataCommandArgs(CommandArgs):
    alias: str
    num: int = -1

    @model_validator(mode="after")
    def validate_data_exists(self):
        if not value_exists_in_dataframes(self.model, self.alias):
            raise Exception(f"File {self.alias} not in dataframes")
        return self

    @model_validator(mode="after")
    def validate_num(self):
        if self.num == -1:
            self.num = maxsize
        return self


class ShowDataCommand(Command):
    def execute(self, args: ShowDataCommandArgs):  # type: ignore
        raise_event("data", args.model.read(args.alias, args.num))
