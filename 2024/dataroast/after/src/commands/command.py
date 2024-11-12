from dataclasses import dataclass

from .factory import cmd_exists, execute_cmd
from .model import Model


@dataclass
class Command:
    cmd: str
    args: list[str | int | list[str]]

    @staticmethod
    def from_string(command: str) -> "Command":
        split_command = command.split()
        cmd = split_command[0]
        args = split_command[1:]
        for i, arg in enumerate(args):
            try:
                if "," in arg:
                    args[i] = arg.split(",")
                elif arg.isnumeric():
                    args[i] = int(arg)
            except ValueError:
                pass

        if not cmd_exists(cmd):
            raise ValueError(f"Command {cmd} does not exist.")

        return Command(cmd, args)

    def execute(self, model: Model) -> None:
        execute_cmd(self.cmd, model, *self.args)
