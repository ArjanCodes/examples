import random
from typing import Callable

type SortFn = Callable[[list[int]], list[int]]


def bubble_sort(data: list[int]) -> list[int]:
    data = data.copy()
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


def quick_sort(data: list[int]) -> list[int]:
    if len(data) <= 1:
        return data.copy()  # Return a copy to ensure immutability

    pivot = data[-1]
    greater: list[int] = [item for item in data[:-1] if item > pivot]
    lesser: list[int] = [item for item in data[:-1] if item <= pivot]
    return quick_sort(lesser) + [pivot] + quick_sort(greater)


def do_operations(data: list[int], sort_fn: SortFn) -> list[int]:
    # multiply each element by 2
    data = [item * 2 for item in data]

    # add a random number to each element
    data = [item + random.randint(-10, 10) for item in data]

    print(f"Data before sorting: {data}")

    result = sort_fn(data)

    print(f"Data after sorting: {data}")
    print(f"Result after sorting: {result}")

    return result


def main() -> None:
    print(do_operations([1, 5, 3, 4, 2], bubble_sort))  # Using Bubble Sort
    print(do_operations([1, 5, 3, 4, 2], quick_sort))  # Using Quick Sort


if __name__ == "__main__":
    main()
