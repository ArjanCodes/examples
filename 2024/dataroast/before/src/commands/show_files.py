from src.commands.command_base import CommandArgs, Command
from src.controller.events import raise_event

from pydantic.dataclasses import dataclass

@dataclass
class ShowFilesCommandArgs(CommandArgs):
    ...

class ShowFilesCommand(Command):

    def execute(self, args: ShowFilesCommandArgs):  # type: ignore
        table_names = args.model.get_table_names()
        if len(table_names) == 0:
            raise_event("files","No files currently stored.")
            return
        
        message = "Files presently stored:"
        for name in table_names:
            message += f"\nAlias: {name}"
        raise_event("files",message)
