from dataclasses import dataclass

from commands.factory import cmd_exists, execute_cmd
from commands.model import Model


@dataclass
class Command:
    cmd: str
    args: list[str | int | list[str]]

    @staticmethod
    def from_string(command: str) -> "Command":
        parts = command.split()
        cmd, raw_args = parts[0], parts[1:]

        # Process each argument, converting to appropriate type
        parsed_args: list[str | int | list[str]] = []
        for i, arg in enumerate(raw_args):
            try:
                if "," in arg:
                    parsed_args[i] = arg.split(",")
                elif arg.isnumeric():
                    parsed_args[i] = int(arg)
            except ValueError:
                pass

        if not cmd_exists(cmd):
            raise ValueError(f"Command {cmd} does not exist.")

        return Command(cmd, parsed_args)

    def execute(self, model: Model) -> None:
        execute_cmd(self.cmd, model, *self.args)
