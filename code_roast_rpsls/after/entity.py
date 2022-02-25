from enum import Enum

from typing_extensions import Self


class ExtendedEnum(Enum):
    @classmethod
    def list(cls) -> list[Self]:
        return [e for e in cls]


class Entity(ExtendedEnum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSOR = "scissor"
    SPOCK = "spock"
    LIZARD = "lizard"

    def __str__(self) -> str:
        return self.value
