"""Factory for creating a game character."""

from typing import Callable, Dict

from game_character import GameCharacter


class GameCharacterFactory:
    """Factory that creates a game character from JSON data."""

    def __init__(self):
        self.creator_fns: Dict[str, Callable[..., GameCharacter]] = {}

    def register(
        self, character_type: str, creator_fn: Callable[..., GameCharacter]
    ) -> None:
        """Register a new game character type."""
        self.creator_fns[character_type] = creator_fn

    def unregister(self, character_type: str) -> None:
        """Unregister a game character type."""
        self.creator_fns.pop(character_type, None)

    def create(self, **kwargs) -> GameCharacter:
        """Create a game character of a specific type, given JSON data."""
        return self.creator_fns[kwargs["type"]](**kwargs)
