import tkinter as tk
from itertools import chain

Point = tuple[float, float]
ShapeData = list[Point]
Color = str


class GraphicsRenderer:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.items: dict[str, int] = {}

    def render(self, shape_id: str, points: ShapeData, color: Color) -> None:
        flat = list(chain.from_iterable(points))
        if shape_id not in self.items:
            self.items[shape_id] = self.canvas.create_polygon(
                flat, fill=color, outline=color
            )
        else:
            item = self.items[shape_id]
            self.canvas.coords(item, *flat)
            self.canvas.itemconfig(item, fill=color, outline=color)

        self.canvas.update()
