import random
from typing import Callable, List

type SortFn = Callable[[List[int]], List[int]]


# Pure function with immutability
def bubble_sort(data: List[int]) -> List[int]:
    sorted_data = data.copy()  # Work with a copy to ensure immutability
    n = len(sorted_data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_data[j] > sorted_data[j + 1]:
                sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]
    return sorted_data


# Pure function with immutability
def quick_sort(data: List[int]) -> List[int]:
    if len(data) <= 1:
        return data.copy()  # Return a copy to ensure immutability
    else:
        pivot = data[-1]
        greater: List[int] = [item for item in data[:-1] if item > pivot]
        lesser: List[int] = [item for item in data[:-1] if item <= pivot]
        return quick_sort(lesser) + [pivot] + quick_sort(greater)


# Pure function: Multiply each element by 2
def multiply_by_2(data: List[int]) -> List[int]:
    return [item * 2 for item in data]


# Pure function: Add a random number to each element
def add_random(data: List[int]) -> List[int]:
    return [item + random.randint(-10, 10) for item in data]


# Function to compose other functions
def compose(
    *functions: Callable[[List[int]], List[int]],
) -> Callable[[List[int]], List[int]]:
    def composed_function(data: List[int]) -> List[int]:
        for function in functions:
            data = function(data)
        return data

    return composed_function


def main() -> None:
    # Compose the operations
    composed_operations = compose(multiply_by_2, add_random)

    # Original data
    data = [1, 5, 3, 4, 2]

    # Using composed operations with bubble sort
    print("Using composed operations with Bubble Sort:")
    transformed_data = composed_operations(data)
    print(f"Data before sorting: {transformed_data}")
    print(f"Result after sorting: {bubble_sort(transformed_data)}")

    # Using composed operations with quick sort
    print("\nUsing composed operations with Quick Sort:")
    transformed_data = composed_operations(data)
    print(f"Data before sorting: {transformed_data}")
    print(f"Result after sorting: {quick_sort(transformed_data)}")

    # Ensure the original data is unchanged
    print(f"\nOriginal data after operations: {data}")


if __name__ == "__main__":
    main()
