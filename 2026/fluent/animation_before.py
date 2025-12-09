import math
from dataclasses import dataclass, field
from typing import Protocol
from graphics import ShapeData, Color, GraphicsRenderer
import time


# ------------------------------------------------------------
# Animation Step Protocol
# ------------------------------------------------------------


class AnimationStep(Protocol):
    def apply(
        self, shape: ShapeData, color: Color, t: float
    ) -> tuple[ShapeData, Color]:
        """
        t ∈ [0, 1] — the local progress through this step.
        """
        ...


# ------------------------------------------------------------
# Helper
# ------------------------------------------------------------


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


# ------------------------------------------------------------
# Concrete Steps (no duration stored here)
# ------------------------------------------------------------


@dataclass
class Move:
    dx: float
    dy: float

    def apply(
        self, shape: ShapeData, color: Color, t: float
    ) -> tuple[ShapeData, Color]:
        new_points = [(x + self.dx * t, y + self.dy * t) for (x, y) in shape]
        return new_points, color


@dataclass
class Rotate:
    angle: float

    def apply(
        self, shape: ShapeData, color: Color, t: float
    ) -> tuple[ShapeData, Color]:
        theta = math.radians(self.angle * t)
        cx = sum(x for x, _ in shape) / len(shape)
        cy = sum(y for _, y in shape) / len(shape)

        out: ShapeData = []
        for x, y in shape:
            nx = cx + (x - cx) * math.cos(theta) - (y - cy) * math.sin(theta)
            ny = cy + (x - cx) * math.sin(theta) + (y - cy) * math.cos(theta)
            out.append((nx, ny))

        return out, color


@dataclass
class Scale:
    factor: float

    def apply(
        self, shape: ShapeData, color: Color, t: float
    ) -> tuple[ShapeData, Color]:
        cx = sum(x for x, _ in shape) / len(shape)
        cy = sum(y for _, y in shape) / len(shape)

        s = lerp(1.0, self.factor, t)
        new_points = [(cx + (x - cx) * s, cy + (y - cy) * s) for (x, y) in shape]

        return new_points, color


@dataclass
class Fade:
    brightness: int  # target grayscale (0–255)

    def apply(
        self, shape: ShapeData, color: Color, t: float
    ) -> tuple[ShapeData, Color]:
        current_val = int(color[1:3], 16)
        new_val = int(lerp(current_val, self.brightness, t))
        new_color = f"#{new_val:02x}{new_val:02x}{new_val:02x}"
        return shape, new_color


# ------------------------------------------------------------
# Animation Timeline (duration now stored here)
# ------------------------------------------------------------


@dataclass
class Animation:
    steps: list[AnimationStep] = field(default_factory=list[AnimationStep])
    durations: list[float] = field(
        default_factory=list[float]
    )
    start_time: float = 0.0

    @property
    def duration(self) -> float:
        return sum(self.durations)

    @property
    def end_time(self) -> float:
        return self.start_time + self.duration


# ------------------------------------------------------------
# Shape with attached animation
# ------------------------------------------------------------


@dataclass
class Shape:
    shape_id: str
    points: ShapeData
    color: Color = "#444444"
    animation: Animation | None = None

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

        # renderer.canvas.update()

        if finished and now >= global_end:
            break

        time.sleep(0.01)
