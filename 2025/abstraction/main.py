from abc import ABC, abstractmethod
from typing import Callable, Protocol

from PIL import Image, ImageOps

# ----------- Callable-based abstraction -----------

# A Callable that takes an Image and returns an Image
ImageFilterFunc = Callable[[Image.Image], Image.Image]


def apply_grayscale(image: Image.Image) -> Image.Image:
    print("Applying grayscale filter (function)...")
    return ImageOps.grayscale(image)


def invert_filter(image: Image.Image) -> Image.Image:
    print("Applying invert filter (function)...")
    return ImageOps.invert(image.convert("RGB"))


def process_with_callable(
    image_path: str, output_path: str, filter_func: ImageFilterFunc
):
    image = Image.open(image_path)
    image = filter_func(image)
    image.save(output_path)
    print(f"Saved processed image to {output_path}")


# ----------- ABC-based abstraction -----------


class FilterBase(ABC):
    @abstractmethod
    def apply(self, image: Image.Image) -> Image.Image: ...


class GrayscaleFilter(FilterBase):
    def apply(self, image: Image.Image) -> Image.Image:
        print("Applying grayscale filter (class)...")
        return ImageOps.grayscale(image)


class InvertFilter(FilterBase):
    def apply(self, image: Image.Image) -> Image.Image:
        print("Applying invert filter (class)...")
        return ImageOps.invert(image.convert("RGB"))


def process_with_abc(image_path: str, output_path: str, filter_obj: FilterBase):
    image = Image.open(image_path)
    image = filter_obj.apply(image)
    image.save(output_path)
    print(f"Saved processed image to {output_path}")


# ----------- Protocol-based abstraction -----------


class ImageFilter(Protocol):
    def apply(self, image: Image.Image) -> Image.Image: ...


# This class doesn't inherit anything but still conforms to the protocol
class SepiaFilter:
    def apply(self, image: Image.Image) -> Image.Image:
        print("Applying sepia filter (class conforming to protocol)...")
        sepia_image = image.convert("RGB")
        width, height = sepia_image.size
        pixels = sepia_image.load()

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))

        return sepia_image


def process_with_protocol(image_path: str, output_path: str, filter_obj: ImageFilter):
    image = Image.open(image_path)
    image = filter_obj.apply(image)
    image.save(output_path)
    print(f"Saved processed image to {output_path}")


def main() -> None:
    input_image = "input.jpg"  # Replace with your image path

    # Callable examples
    process_with_callable(input_image, "output_callable_grayscale.jpg", apply_grayscale)
    process_with_callable(input_image, "output_callable_invert.jpg", invert_filter)

    # ABC examples
    process_with_abc(input_image, "output_abc_grayscale.jpg", GrayscaleFilter())
    process_with_abc(input_image, "output_abc_invert.jpg", InvertFilter())

    # Protocol example
    process_with_protocol(input_image, "output_protocol_sepia.jpg", SepiaFilter())


if __name__ == "__main__":
    main()
