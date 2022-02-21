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


def main():
    circle = Circle(radius=2)
    print(circle)
    print(f"Circumference: {circle.circumference}")


if __name__ == "__main__":
    main()
