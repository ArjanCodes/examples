from typing import Protocol

class View(Protocol):
    def run(self):
        ...
    
    def display_message(self,message:str):
        ...