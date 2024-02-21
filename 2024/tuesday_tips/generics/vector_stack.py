from stack import Stack


class VectorStack[T: (int, float)](Stack[T]):
    def __getitem__(self, index: int) -> T:
        return self._container[index]

    def __setitem__(self, index: int, value: T) -> None:
        if 0 <= index < len(self._container):
            self._container[index] = value
        else:
            raise IndexError("Stack index out of range")
