from typing import Self


class Rectangle:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

    def __mul__(self, other: Self) -> Self:
        if isinstance(other, Rectangle):
            return Rectangle(self.width * other.width, self.height * other.height)
        elif isinstance(other, int) or isinstance(other, float):
            return Rectangle(self.width * other, self.height * other)

    def __eq__(self, other: Self) -> bool:
        return self.width == other.width and self.height == other.height

    def __repr__(self) -> str:
        return f"Rectangle({self.width}, {self.height})"


def main() -> None:
    r1 = Rectangle(10, 20)
    r2 = Rectangle(2, 3)
    print(r1 * r2)  # Yay! We can multiply rectangles now!


if __name__ == "__main__":
    main()
