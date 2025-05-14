from typing import Any

from PIL import Image, ImageOps


class InvertFilter:
    def __init__(self) -> None:
        self._enabled: bool = True

    @property
    def name(self) -> str:
        return "Invert"

    def apply(self, image: Image.Image) -> Image.Image:
        if self._enabled:
            print(f"Applying {self.name} filter")
            return ImageOps.invert(image.convert("RGB"))
        else:
            print(f"{self.name} filter disabled, returning original image")
            return image

    def configure(self, config: dict[str, Any]) -> None:
        self._enabled = config.get("enabled", self._enabled)
