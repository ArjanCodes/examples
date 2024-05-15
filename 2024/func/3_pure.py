import random
from typing import Callable

type SortFn = Callable[[list[int]], list[int]]


def bubble_sort(data: list[int]) -> list[int]:
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


def quick_sort(data: list[int]) -> list[int]:
    if len(data) <= 1:
        return data

    pivot = data[-1]
    greater = [item for item in data[:-1] if item > pivot]
    lesser = [item for item in data[:-1] if item <= pivot]
    return quick_sort(lesser) + [pivot] + quick_sort(greater)


def do_operations(data: list[int]) -> list[int]:
    # multiply each element by 2
    data = [item * 2 for item in data]

    # add a random number to each element
    data = [item + random.randint(-10, 10) for item in data]

    return bubble_sort(data)


def main() -> None:
    data = [1, 5, 3, 4, 2]
    print(f"Data before sorting: {data}")

    result = do_operations(data)

    print(f"Result after sorting: {result}")


if __name__ == "__main__":
    main()
