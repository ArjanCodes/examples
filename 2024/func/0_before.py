import random
from typing import Callable

type SortFn = Callable[[list[int]], list[int]]


def bubble_sort(data: list[int]) -> list[int]:
    print(f"Data before sorting: {data}")
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    print(f"Data after sorting: {data}")
    return data


def do_operations(data: list[int]):
    # multiply each element by 2
    data = [item * 2 for item in data]

    # add a random number to each element
    data = [item + random.randint(-10, 10) for item in data]

    result = bubble_sort(data)

    print(f"Result after sorting: {result}")


def main() -> None:
    do_operations([1, 5, 3, 4, 2])


if __name__ == "__main__":
    main()
