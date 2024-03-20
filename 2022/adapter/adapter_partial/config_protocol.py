from typing import Any, Protocol


class Config(Protocol):
    def get(self, key: str, default: Any = None) -> Any | None: ...
