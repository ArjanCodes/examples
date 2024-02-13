from typing import TypeVar
from stack import Stack

T = TypeVar('T', int, float)


class VectorStack(Stack[T]):
    def __getitem__(self, index: int) -> T:
        return self._container[index]

    def __setitem__(self, index: int, value: T) -> None:
        if 0 <= index < len(self._container):
            self._container[index] = value
        else:
            raise IndexError("Stack index out of range")
