"""
Basic example showing how to create objects from data using a dynamic factory with
register/unregister methods.
"""

import importlib
import json
from typing import List

from game_character import GameCharacter
from game_character_factory import GameCharacterFactory


class Sorcerer(GameCharacter):
    """Represents a sorcerer game character."""

    def make_a_noise(self):
        print("Aaaargh!")


class Wizard(GameCharacter):
    """Represents a wizard game character."""

    def make_a_noise(self):
        print("Boohh!")


class Fighter(GameCharacter):
    """Represents a fighter game character."""

    def make_a_noise(self):
        print("Bam!")


class ModuleInterface:
    """Represents a plugin interface. A plugin has a single register function."""

    @staticmethod
    def register(factory: GameCharacterFactory) -> None:
        """Register the necessary items in the game character factory."""


def import_module(name: str) -> ModuleInterface:
    """Imports a module given a name."""
    return importlib.import_module(name)  # type: ignore


def load_plugins(factory: GameCharacterFactory, plugins: List[str]) -> None:
    """Loads the plugins defined in the plugins list."""
    for plugin_file in plugins:
        plugin = import_module(plugin_file)
        plugin.register(factory)


def main() -> None:
    """Main function."""

    # game character factory
    factory = GameCharacterFactory()

    # register a couple of character types
    factory.register("sorcerer", Sorcerer)
    factory.register("wizard", Wizard)
    factory.register("fighter", Fighter)

    # read data from a JSON file
    characters: List[GameCharacter] = []
    with open("./data.json") as file:
        data = json.load(file)

        # load the plugins
        load_plugins(factory, data["plugins"])

        # create the characters
        characters = [factory.create(**item) for item in data["characters"]]

    # do something with the characters
    print(characters)
    for charactor in characters:
        charactor.make_a_noise()


if __name__ == "__main__":
    main()
