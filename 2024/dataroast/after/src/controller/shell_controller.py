from commands.factory import COMMANDS
from controller.controller import Controller
from controller.events import register_event
from view.view import View


class ShellController(Controller):
    def __init__(self, model, view: View) -> None:
        super().__init__(model, view)

        for command in COMMANDS.keys():
            register_event(command, view.display_message)

        view.run()
