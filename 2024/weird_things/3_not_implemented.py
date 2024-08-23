from dataclasses import dataclass


class Shape:
    def area(self) -> float:
        raise NotImplementedError("Subclasses must implement this method")


@dataclass
class Rectangle(Shape):
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rectangle):
            return NotImplemented  # Indicates the comparison is not implemented for this type
        return self.area() == other.area()


def main() -> None:
    # Testing NotImplementedError
    try:
        # This will raise NotImplementedError since 'area' is not implemented
        c = Shape()
        c.area()
    except NotImplementedError as e:
        print(e)  # Output: Subclasses must implement this method

    # Testing NotImplemented
    r1 = Rectangle(2, 3)
    r2 = Rectangle(2, 3)
    r3 = "not a rectangle"

    print(r1 == r2)  # Output: True, since areas are the same
    print(
        r1 == r3
    )  # Output: False, NotImplemented is returned and Python falls back to other methods of comparison


if __name__ == "__main__":
    main()
