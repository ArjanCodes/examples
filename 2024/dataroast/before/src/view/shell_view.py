from src.model.model import Model
from src.commands.command_base import CommandArgs, Command
import src.commands.factory as factory


def _parse_commands(model:Model,commands: str) -> tuple[Command, CommandArgs]:
    split_commands = commands.split()
    command = split_commands[0]
    arguments = [args for args in split_commands[1:] if args != '']
    command, arguments = factory.generate_cmd_and_args(model, command, arguments)

    return command, arguments


class Shell:
    def __init__(self, model: Model) -> None:
        self.model = model

    def run(self):
        while True:
            user_input = input("tell me what you want ")
            try:
                command, args = _parse_commands(self.model,user_input)
            except TypeError as e:
                self.display_message(f"Incorrect args provided for command")
                self.display_message(e)
            else:
                command.execute(args)
    
    def display_message(self,message):
        print(message)