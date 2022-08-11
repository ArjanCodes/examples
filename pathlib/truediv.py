from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def __truediv__(self, other: float) -> Point:
        return Point(self.x / other, self.y / other)


def main() -> None:
    p = Point(1, 2)
    print(p / 2)


if __name__ == "__main__":
    main()
