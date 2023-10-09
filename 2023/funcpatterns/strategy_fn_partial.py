import random
from typing import Callable
from functools import partial


def bubble_sort(data: list[int]) -> list[int]:
    data = data.copy()
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


def quick_sort(data: list[int]) -> list[int]:
    data = data.copy()
    if len(data) <= 1:
        return data
    else:
        pivot = data.pop()
        greater: list[int] = []
        lesser: list[int] = []
        for item in data:
            if item > pivot:
                greater.append(item)
            else:
                lesser.append(item)
        return quick_sort(lesser) + [pivot] + quick_sort(greater)


SortFn = Callable[[list[int]], list[int]]


def context(strategy: SortFn, data: list[int]) -> list[int]:
    # multiply each element by 2
    data = [item * 2 for item in data]

    # add a random number to each element
    data = [item + random.randint(-10, 10) for item in data]

    return strategy(data)


def main() -> None:
    bubble_sort_context = partial(context, bubble_sort)
    print(bubble_sort_context([1, 5, 3, 4, 2]))  # Using Bubble Sort
    print(context(quick_sort, [1, 5, 3, 4, 2]))  # Using Quick Sort


if __name__ == "__main__":
    main()
