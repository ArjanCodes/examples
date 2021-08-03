"""
Basic example showing how to create objects from data using a dynamic factory with
register/unregister methods.
"""

import json
from dataclasses import dataclass

from game.character import GameCharacter


@dataclass
class Sorcerer:

    name: str

    def make_a_noise(self) -> None:
        print("Aaaargh!")


@dataclass
class Wizard:

    name: str

    def make_a_noise(self) -> None:
        print("Boohh!")


@dataclass
class Witcher:

    name: str

    def make_a_noise(self) -> None:
        print("Bam!")


def main() -> None:
    """Creates game characters from a file containg a level definition."""

    # read data from a JSON file
    with open("./level.json") as file:
        data = json.load(file)

        # create the characters
        characters: list[GameCharacter] = []
        for item in data["characters"]:
            character_type = item["type"]
            del item["type"]
            if character_type == "sorcerer":
                characters.append(Sorcerer(item))
            elif character_type == "wizard":
                characters.append(Wizard(item))
            elif character_type == "witcher":
                characters.append(Witcher(item))

        # do something with the characters
        for character in characters:
            character.make_a_noise()


if __name__ == "__main__":
    main()
