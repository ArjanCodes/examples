import timeit


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.x, self.y))


def main() -> None:
    # Create a large collection of Point objects
    points = [Point(x, x) for x in range(100000)]

    # Check if a specific point exists in the collection
    target_point = Point(500, 500)

    execution_time = timeit.timeit(lambda: target_point in points, number=10000)
    print(f"Execution time: {execution_time} seconds")


if __name__ == "__main__":
    main()
