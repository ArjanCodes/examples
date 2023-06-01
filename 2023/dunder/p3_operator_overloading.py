from dataclasses import dataclass
from typing import Self


class Vector:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Self) -> Self:
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"


def main() -> None:
    a = Vector(1, 2)
    b = Vector(3, 4)
    d = Vector(1, 2)
    c = a + b
    print(c)  # Output: Vector(4, 6)
    print(a == b)  # Output: False
    print(a == d)  # Output: True


if __name__ == "__main__":
    main()
