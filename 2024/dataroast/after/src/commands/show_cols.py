from src.commands.validations import value_exists_in_dataframes
from src.commands.command_base import CommandArgs, Command
from src.controller.events import raise_event

from pydantic.dataclasses import dataclass
from pydantic import model_validator


@dataclass
class ShowColsCommandArgs(CommandArgs):

    alias: str

    @model_validator(mode='after')
    def validate_data_exists(self):
        if not value_exists_in_dataframes(self.model,self.alias):
            raise Exception(f"File {self.alias} not in dataframes")
        return self

class ShowColsCommand(Command):

    def execute(self, args: ShowColsCommandArgs):  # type: ignore
        raise_event('cols',args.model.read(args.alias).columns.values)
