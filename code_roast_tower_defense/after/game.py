import tkinter as tk
from abc import ABC, abstractmethod
from typing import Protocol


class GameObject(Protocol):
    def update(self):
        """Updates the game."""

    def paint(self, canvas: tk.Canvas):
        """Paints the game."""


class Game(ABC):  # the main class that we call "Game"
    def __init__(
        self, title: str, width: int, height: int, timestep: int = 50
    ):  # setting up the window for the game here
        self.root = tk.Tk()  # saying this window will use tkinter
        self.root.title(title)
        self.running = True  # creating a variable RUN. does nothing yet.
        self.root.protocol("WM_DELETE_WINDOW", self.end)
        self.timestep = timestep
        self.frame = tk.Frame(master=self.root)
        self.frame.grid(row=0, column=0)

        self.canvas = tk.Canvas(
            master=self.frame,
            width=width,
            height=height,
            bg="white",
            highlightthickness=0,
        )  # actually creates a window and puts our frame on it
        self.canvas.grid(
            row=0, column=0, rowspan=2, columnspan=1
        )  # makes the window called "canvas" complete

        self.objects: list[GameObject] = []

    def add_object(self, obj: GameObject):
        self.objects.append(obj)

    def remove_object(self, obj: GameObject):
        self.objects.remove(obj)

    def run(self):
        self.initialize()
        self._run()
        self.root.mainloop()

    def _run(self):
        if not self.running:
            return
        self.update()  # calls the function 'def update(self):'
        self.canvas.delete(tk.ALL)  # clear the screen
        self.paint()  # calls the function 'def paint(self):'

        self.root.after(
            self.timestep, self._run
        )  # does a run of the function every 50/1000 = 1/20 of a second

    def end(self):
        self.root.destroy()  # closes the game window and ends the program

    def initialize(self):
        """Initializes the game."""

    def update(self):
        """Updates the game."""
        for obj in self.objects:
            obj.update()

    def paint(self):
        """Paints the game."""
        for obj in self.objects:
            obj.paint(self.canvas)
