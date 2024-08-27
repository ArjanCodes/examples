from collections import deque
from typing import Callable, Sequence
from decimal import Decimal
from typing import TypeVar

# Using a custom defined type variable to represent a numeric type

Numeric = TypeVar("Numeric", bound=int | float | Decimal)


# Makes the function generic
# It can handle a certain type and then return a list of the same type
# Try using generics to the smallest parts as possible
# For example, do not use a generic type for list[int | float | Decimal]
# Instead, use a generic type for int, float, and Decimal separately
# This way, the function is more readable and easier to understand
def merge_sort(arr: list[Numeric]) -> list[Numeric]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)


def merge(left: list[Numeric], right: list[Numeric]) -> list[Numeric]:
    sorted_arr: list[Numeric] = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1

    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])

    return sorted_arr


# Inline basic example with one generic type for 3.12 and above


def reverse_real_queue[T](queue: deque[T]) -> deque[T]:
    return deque(reversed(queue))


# More advanced example with two generic types for 3.12 and above


# The type that is return from the transform function
# is going to be returned from the callable function
def transform_matrix[T, R](
    matrix: Sequence[Sequence[T]], transform: Callable[[T], R]
) -> list[list[R]]:
    return [[transform(element) for element in row] for row in matrix]
