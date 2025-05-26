from typing import Any

from PIL import Image, ImageOps

from .base import FilterBase


class GrayscaleFilter(FilterBase):
    def __init__(self) -> None:
        self._intensity: float = 1.0

    @property
    def name(self) -> str:
        return "Grayscale"

    def apply(self, image: Image.Image) -> Image.Image:
        print(f"Applying {self.name} filter with intensity {self._intensity}")
        grayscale_image = ImageOps.grayscale(image).convert("RGB")
        if self._intensity < 1.0:
            return Image.blend(image, grayscale_image, self._intensity)
        return grayscale_image

    def configure(self, config: dict[str, Any]) -> None:
        self._intensity = config.get("intensity", self._intensity)
