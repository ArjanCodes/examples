from typing import Any, Protocol


class Config(Protocol):
    def get(self, key: str) -> Any | None: ...
