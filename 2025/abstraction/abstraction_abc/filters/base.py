from abc import ABC, abstractmethod
from typing import Any

from PIL import Image


class FilterBase(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def apply(self, image: Image.Image) -> Image.Image: ...

    @abstractmethod
    def configure(self, config: dict[str, Any]) -> None: ...
