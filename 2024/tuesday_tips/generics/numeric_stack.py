from typing import Literal
from stack import Stack


class NumericStack[T: (int, float)](Stack[T]):
    def __getitem__(self, index: int) -> T:
        return self._container[index]

    def __setitem__(self, index: int, value: T) -> None:
        if 0 <= index < len(self._container):
            self._container[index] = value
        else:
            raise IndexError("Stack index out of range")

    def sum(self) -> T | Literal[0]:
        return sum(self._container)

    def average(self) -> float:
        if self.is_empty():
            return 0

        total: T | Literal[0] = self.sum()

        return total / self.size()

    def max(self) -> T | None:
        if self.is_empty():
            return None
        return max(self._container)

    def min(self) -> T | None:
        if self.is_empty():
            return None
        return min(self._container)
