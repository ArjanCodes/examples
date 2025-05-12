from .base import FilterBase
from PIL import Image, ImageOps
from typing import Any

class GrayscaleFilter(FilterBase):
    def __init__(self) -> None:
        self._intensity: float = 1.0

    @property
    def name(self) -> str:
        return "Grayscale"

    def apply(self, image: Image.Image) -> Image.Image:
        print(f"Applying {self.name} filter with intensity {self._intensity}")
        return ImageOps.grayscale(image)

    def configure(self, config: dict[str, Any]) -> None:
        self._intensity = config.get("intensity", self._intensity)