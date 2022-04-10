from enum import Enum


class Entity(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSOR = "scissor"
    SPOCK = "spock"
    LIZARD = "lizard"

    def __str__(self) -> str:
        return self.value
