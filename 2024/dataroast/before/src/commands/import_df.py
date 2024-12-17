from src.commands.command_base import CommandArgs, Command
from src.commands.validations import path_exists
from src.controller.events import raise_event

import pandas as pd
from pydantic import field_validator
from pydantic.dataclasses import dataclass


@dataclass
class ImportCommandArgs(CommandArgs):
    alias: str
    path: str

    @field_validator("path")
    def validate_path(cls, value):
        if not path_exists(value):
            raise Exception(f"File not found at path: {value}")
        return value


class ImportCommand(Command):
    def execute(self, args: ImportCommandArgs):  # type: ignore
        df = pd.read_csv(args.path)
        args.model.create(args.alias, df)
        raise_event("import", "Imported!")
