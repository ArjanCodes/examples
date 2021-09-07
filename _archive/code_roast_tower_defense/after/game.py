import tkinter as tk
from typing import Optional, Protocol


class GameObject(Protocol):
    def update(self):
        """Updates the game."""

    def paint(self, canvas: tk.Canvas):
        """Paints the game."""


class Game:  # the main class that we call "Game"
    def __init__(
        self, title: str, width: int, height: int, timestep: int = 50
    ):  # setting up the window for the game here
        self.root = tk.Tk()  # saying this window will use tkinter
        self.root.title(title)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.end)
        self.timer_id: Optional[str] = None
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
        self.running = True
        self._run()
        self.root.mainloop()

    def _run(self):
        self.update()
        self.paint()

        if self.running:
            self.timer_id = self.root.after(self.timestep, self._run)

    def end(self):
        self.running = False
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
        self.root.destroy()

    def update(self):
        """Updates the game."""
        for obj in self.objects:
            obj.update()

    def paint(self):
        """Paints the game."""
        self.canvas.delete(tk.ALL)  # clear the screen
        for obj in self.objects:
            obj.paint(self.canvas)
