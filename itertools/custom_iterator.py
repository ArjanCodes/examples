from dataclasses import dataclass
from typing import Self


@dataclass
class NumberIterator:
    max: int
    num: int = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> int:
        if self.num >= self.max:
            raise StopIteration
        self.num += 1
        return self.num


@dataclass
class InfiniteNumberIterator:
    num: int = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> int:
        self.num += 1
        return self.num


def main() -> None:
    for num in NumberIterator(3):
        print(num)


if __name__ == "__main__":
    main()
