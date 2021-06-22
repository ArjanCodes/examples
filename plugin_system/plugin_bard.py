"""Game extension that adds a bard character."""

from game_character import GameCharacter
from game_character_factory import GameCharacterFactory


class Bard(GameCharacter):
    """Represents a bard game character."""

    def make_a_noise(self):
        print("Toss a coin to the Witcher!")


def register(factory: GameCharacterFactory):
    """Registers the plugin-specific things."""
    factory.register("bard", Bard)
