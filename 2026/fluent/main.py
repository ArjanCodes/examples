

import time
import tkinter as tk
from typing import Any

from graphics import GraphicsRenderer
from animation import Shape, Animation


def play_scene(renderer: GraphicsRenderer, shapes: list[Shape]) -> None:
    animations = [s.animation for s in shapes if s.animation is not None]
    if not animations:
        return


    global_end = max(anim.end_time for anim in animations)
    t0 = time.time()

    while True:
        now = time.time() - t0
        finished = True

        for shape in shapes:
            anim = shape.animation
            if anim is None:
                continue

            # Active?
            if not (anim.start_time <= now <= anim.end_time):
                continue

            finished = False

            # Time inside this animation
            t_anim = now - anim.start_time
            time_cursor = 0.0

            # Always start computations from the original state
            points = shape.points
            color = shape.color

            for step, duration in zip(anim.steps, anim.durations):
                if duration <= 0:
                    continue

                local_t_raw = (t_anim - time_cursor) / duration
                local_t = max(0.0, min(1.0, local_t_raw))

                points, color = step.apply(points, color, local_t)

                # If we are still inside this step, it means this is the active one → stop
                if local_t < 1.0:
                    break

                time_cursor += duration

            renderer.render(shape.shape_id, points, color)

        renderer.canvas.update()

        if finished and now >= global_end:
            break

        time.sleep(0.01)

def main() -> None:
    root = tk.Tk()
    root.title("ShapyMcShapeface Renderer")

    canvas_width = 800
    canvas_height = 600

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()

    renderer = GraphicsRenderer(canvas)

    square = Shape(
        shape_id="square",
        points=[(250, 200), (350, 200), (350, 300), (250, 300)],
        color="#444444",
        animation=(
            Animation(start_time=0.0)
            .rotate(60, duration=1.0)
            .move(200, 0, duration=1.0)
            .scale(1.3, duration=1.0)
            .fade_to(200, duration=0.8)
            .move(0, 120, duration=1.0)
            .fade_to(40, duration=0.8)
        ),
    )

    triangle = Shape(
        shape_id="triangle",
        points=[(500, 250), (550, 350), (450, 350)],
        color="#888888",
        animation=(
            Animation(start_time=0.5)
            .fade_to(220, duration=1.0)
            .move(-80, 40, duration=1.0)
            .scale(0.9, duration=1.0)
        ),
    )

    shapes = [square, triangle]

    def start_animation(event: Any):
        play_scene(renderer, shapes)

    # Start on click or keypress
    canvas.bind("<Button-1>", start_animation)
    root.bind("<Key>", start_animation)

    root.mainloop()


if __name__ == "__main__":
    main()