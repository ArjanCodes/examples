from commands.command import Command
from commands.model import Model


class Shell:
    def __init__(self, model: Model) -> None:
        self.model = model

    def run(self):
        while True:
            user_input = input(">> ")
            try:
                command = Command.from_string(user_input)
                command.execute(self.model)
            except TypeError as e:
                self.display_message("Incorrect args provided for command")
                self.display_log(e)

    def display_message(self, message: str) -> None:
        print(message)

    def display_log(self, exception: Exception) -> None:
        print(exception)
