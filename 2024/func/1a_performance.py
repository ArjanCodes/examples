from random import randint
from time import perf_counter


def bubble_sort(data: list[int]) -> list[int]:
    n = len(data)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True

        if not swapped:
            break
    return data


def quick_sort(data: list[int]) -> list[int]:
    if len(data) <= 1:
        return data.copy()

    pivot = data[-1]
    greater = [item for item in data[:-1] if item > pivot]
    lesser = [item for item in data[:-1] if item <= pivot]
    return quick_sort(lesser) + [pivot] + quick_sort(greater)


def partition(data: list[int], low: int, high: int) -> int:
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
    data[i + 1], data[high] = data[high], data[i + 1]
    return i + 1


def quick_sort_iterative(data: list[int]) -> list[int]:
    sorted_data = data.copy()  # Work with a copy to ensure immutability
    stack: list[tuple[int, int]] = [(0, len(sorted_data) - 1)]

    while stack:
        low, high = stack.pop()
        if low < high:
            p = partition(sorted_data, low, high)
            stack.append((low, p - 1))
            stack.append((p + 1, high))

    return sorted_data


def main() -> None:
    data = [randint(0, 10000) for _ in range(10000)]

    start = perf_counter()
    quick_sort(data)
    print(f"Time taken for recursive quick sort: {perf_counter() - start:.6f} seconds")

    start = perf_counter()
    sorted = quick_sort_iterative(data)
    print(f"Time taken for iterative quick sort: {perf_counter() - start:.6f} seconds")

    start = perf_counter()
    bubble_sort(sorted)
    print(f"Time taken for bubble sort: {perf_counter() - start:.6f} seconds")


if __name__ == "__main__":
    main()
