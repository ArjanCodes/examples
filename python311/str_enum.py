from enum import StrEnum, auto


class Color(StrEnum):
    WHITE = auto()
    BLACK = auto()


print(Color.BLACK.value)
