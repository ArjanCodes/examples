class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


def main() -> None:
    point = Point(3, 4)
    print(point)  # Output: Point(3, 4)


if __name__ == "__main__":
    main()
