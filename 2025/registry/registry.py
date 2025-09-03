
from typing import Callable

_registry: list[tuple[str, str, Callable[..., None]]] = []

def register_command(group: str, name: str):
    def decorator(func: Callable[..., None]):
        _registry.append((group, name, func))
        return func
    return decorator

def get_registry() -> list[tuple[str, str, Callable[..., None]]]:
    return _registry.copy()
