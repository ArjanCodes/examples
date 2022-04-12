from typing import Protocol

from bs4 import NavigableString


class BSElement(Protocol):
    def get_text(self) -> str:
        ...


class BS(Protocol):
    def find(self, name: str) -> BSElement | NavigableString | None:
        ...
