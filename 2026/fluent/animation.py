import math
from dataclasses import dataclass, field
from typing import Protocol, Self
from graphics import ShapeData, Color


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

    def add(self, step: AnimationStep, duration: float) -> Self:
        self.steps.append(step)
        self.durations.append(duration)
        return self

    # fluent API
    def move(self, dx: float, dy: float, duration: float = 0.5) -> Self:
        return self.add(Move(dx, dy), duration)

    def rotate(self, angle: float, duration: float = 1.0) -> Self:
        return self.add(Rotate(angle), duration)

    def scale(self, factor: float, duration: float = 0.5) -> Self:
        return self.add(Scale(factor), duration)

    def fade_to(self, brightness: int, duration: float = 0.5) -> Self:
        return self.add(Fade(brightness), duration)

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
