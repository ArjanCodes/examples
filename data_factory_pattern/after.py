"""
Basic example showing how to create objects from data using a dynamic factory with
register/unregister methods.
"""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass
class GameCharacter(ABC):
    """Basic representation of a game character with a class and a name."""

    type: str
    name: str

    @abstractmethod
    def make_a_noise(self):
        """Let the character make a noise."""


class Sorcerer(GameCharacter):
    def make_a_noise(self):
        print("Aaaargh!")


class Wizard(GameCharacter):
    def make_a_noise(self):
        print("Boohh!")


class Fighter(GameCharacter):
    def make_a_noise(self):
        print("Bam!")


class Bard(GameCharacter):
    def make_a_noise(self):
        print("Toss a coin!")


class GameCharacterFactory:
    def __init__(self):
        self.creator_fns: Dict[str, Callable[..., GameCharacter]] = {}

    def register(
        self, character_type: str, creator_fn: Callable[..., GameCharacter]
    ) -> None:
        self.creator_fns[character_type] = creator_fn

    def unregister(self, character_type: str) -> None:
        self.creator_fns.pop(character_type, None)

    def create(self, **kwargs) -> GameCharacter:
        return self.creator_fns[kwargs["type"]](**kwargs)


def main() -> None:
    """Main function."""

    # game character factory
    factory = GameCharacterFactory()

    # register the various character types
    factory.register("sorcerer", Sorcerer)
    factory.register("wizard", Wizard)
    factory.register("fighter", Fighter)
    factory.register("bard", Bard)

    # read data from a JSON file to create the game characters
    characters: List[GameCharacter] = []
    with open("./data.json") as file:
        data = json.load(file)
        characters = [factory.create(**item) for item in data]

    # do something with the characters
    print(characters)
    for charactor in characters:
        charactor.make_a_noise()


if __name__ == "__main__":
    main()
