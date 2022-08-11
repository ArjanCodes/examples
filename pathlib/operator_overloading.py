from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def __truediv__(self, other: float) -> Point:
        return Point(self.x / other, self.y / other)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


def main() -> None:
    point = Point(1, 2)
    print(point / 2)
    print(point + point)


if __name__ == "__main__":
    main()
