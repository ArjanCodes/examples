import tkinter as tk
from typing import Any

from graphics import GraphicsRenderer
from animation_before import Shape, Animation, play_scene, Rotate, Move, Scale, Fade




def main() -> None:
    root = tk.Tk()
    root.title("ShapyMcShapeface Renderer")

    canvas_width = 800
    canvas_height = 600

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()

    renderer = GraphicsRenderer(canvas)

    # ------------------------------------------------------------
    # Square animation (non-fluent, defined in a single expression)
    # ------------------------------------------------------------

    square_animation = Animation(
        steps=[
            Rotate(60),
            Move(200, 0),
            Scale(1.3),
            Fade(200),
            Move(0, 120),
            Fade(40),
        ],
        durations=[
            1.0,   # rotate
            1.0,   # move right
            1.0,   # scale
            0.8,   # fade to 200
            1.0,   # move downward
            0.8,   # fade to 40
        ],
        start_time=0.0,
    )

    square = Shape(
        shape_id="square",
        points=[(250, 200), (350, 200), (350, 300), (250, 300)],
        color="#444444",
        animation=square_animation,
    )

    # ------------------------------------------------------------
    # Triangle animation (non-fluent, also one expression)
    # ------------------------------------------------------------

    triangle_animation = Animation(
        steps=[
            Fade(220),
            Move(-80, 40),
            Scale(0.9),
        ],
        durations=[
            1.0,   # fade
            1.0,   # move up-left
            1.0,   # scale down
        ],
        start_time=0.5,
    )

    triangle = Shape(
        shape_id="triangle",
        points=[(500, 250), (550, 350), (450, 350)],
        color="#888888",
        animation=triangle_animation,
    )

    shapes = [square, triangle]

    # ------------------------------------------------------------
    # Event binding
    # ------------------------------------------------------------

    def start_animation(event: Any):
        play_scene(renderer, shapes)

    canvas.bind("<Button-1>", start_animation)
    root.bind("<Key>", start_animation)

    root.mainloop()

if __name__ == "__main__":
    main()