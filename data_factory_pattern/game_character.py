"""Represents a basic game character."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class GameCharacter(ABC):
    """Basic representation of a game character with a class and a name."""

    type: str
    name: str

    @abstractmethod
    def make_a_noise(self):
        """Let the character make a noise."""
