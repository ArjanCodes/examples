from abc import ABC, abstractmethod
from typing import Any

from PIL import Image, ImageOps


class FilterBase(ABC):
    name: str

    @abstractmethod
    def apply(self, image: Image.Image) -> Image.Image: ...

    @abstractmethod
    def configure(self, config: dict[str, Any]) -> None: ...


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


class InvertFilter(FilterBase):
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


def process_with_abc(image_path: str, output_path: str, filter_obj: FilterBase) -> None:
    print(f"\nUsing filter: {filter_obj.name}")
    image = Image.open(image_path)
    image = filter_obj.apply(image)
    image.save(output_path)
    print(f"Saved processed image to {output_path}")


def main() -> None:
    input_image: str = "input.jpg"

    grayscale = GrayscaleFilter()
    grayscale.configure({"intensity": 0.8})
    process_with_abc(input_image, "output_abc_grayscale.jpg", grayscale)

    invert = InvertFilter()
    invert.configure({"enabled": True})
    process_with_abc(input_image, "output_abc_invert.jpg", invert)


if __name__ == "__main__":
    main()
