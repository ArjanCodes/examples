from dataclasses import dataclass
from math import pi


@dataclass
class Circle:
    x: float = 0
    y: float = 0
    radius: float = 1

    @property
    def circumference(self) -> float:
        return 2 * self.radius * pi


circle = Circle(radius=2)
print(f"Circumference: {circle.circumference}")
