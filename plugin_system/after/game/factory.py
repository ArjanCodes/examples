"""Factory for creating a game character."""

from typing import Any, Callable

from game.character import GameCharacter

creator_fns: dict[str, Callable[..., GameCharacter]] = {}


def register(character_type: str, creator_fn: Callable[..., GameCharacter]) -> None:
    """Register a new game character type."""
    creator_fns[character_type] = creator_fn


def unregister(character_type: str) -> None:
    """Unregister a game character type."""
    creator_fns.pop(character_type, None)


def create(arguments: dict[str, Any]) -> GameCharacter:
    """Create a game character of a specific type, given JSON data."""
    args_copy = arguments.copy()
    character_type = args_copy.pop("type")
    try:
        creator_func = creator_fns[character_type]
    except KeyError:
        raise ValueError(f"unknown character type {character_type!r}") from None
    return creator_func(**args_copy)
