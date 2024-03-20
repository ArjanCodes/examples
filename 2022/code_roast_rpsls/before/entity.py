from enum import Enum, auto


class Entity(Enum):
    ROCK = auto()
    PAPER = auto()
    SCISSOR = auto()
    SPOCK = auto()
    LIZARD = auto()

    def __repr__(self) -> str:
        return f"{self.name} : {self.value}"
