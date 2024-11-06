from src.controller.controller import Controller
from src.controller.events import register_event
from src.view.view import View
from src.commands.factory import COMMANDS

class ShellController(Controller):
    def __init__(self, model, view: View) -> None:
        super().__init__(model, view)

        for command in COMMANDS.keys():
            register_event(command,view.display_message)
        
        view.run()