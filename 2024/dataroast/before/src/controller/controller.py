from src.view.view import View
from src.controller.events import clear_events

class Controller:
    '''Remember to call view.run() in each inheriting class at the end of the init method'''
    def __init__(self, model, view: View) -> None:
        self.model = model
        self.view = view

        clear_events()