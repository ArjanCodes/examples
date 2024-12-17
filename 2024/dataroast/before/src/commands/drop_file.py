from src.controller.events import raise_event
from src.commands.validations import value_exists_in_dataframes
from src.commands.command_base import CommandArgs, Command

from pydantic.dataclasses import dataclass
from pydantic import model_validator


@dataclass
class DropFileCommandArgs(CommandArgs):
    alias: str

    @model_validator(mode="after")
    def validate_data_exists(self):
        if not value_exists_in_dataframes(self.model, self.alias):
            raise Exception(f"File {self.alias} not in dataframes")
        return self


class DropFileCommand(Command):
    def execute(self, args: DropFileCommandArgs):  # type: ignore
        raise_event("drop", f"Dropping {args.alias}")
        args.model.delete(args.alias)
        raise_event("drop", f"Remaining files: {args.model.get_table_names()}")
