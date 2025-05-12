from abc import ABC, abstractmethod
from PIL import Image
from typing import Any

class FilterBase(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def apply(self, image: Image.Image) -> Image.Image: ...

    @abstractmethod
    def configure(self, config: dict[str, Any]) -> None: ...