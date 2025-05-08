from typing import Any, Protocol

from PIL import Image


class ImageFilter(Protocol):
    name: str

    def apply(self, image: Image.Image) -> Image.Image: ...

    def configure(self, config: dict[str, Any]) -> None: ...


class SepiaFilter:
    def __init__(self) -> None:
        self._depth: int = 20

    @property
    def name(self) -> str:
        return "Sepia"

    def apply(self, image: Image.Image) -> Image.Image:
        print(f"Applying {self.name} filter with depth {self._depth}")
        sepia_image = image.convert("RGB")
        width, height = sepia_image.size
        pixels = sepia_image.load()

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b + self._depth)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b + self._depth)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b + self._depth)
                pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))

        return sepia_image

    def configure(self, config: dict[str, Any]) -> None:
        self._depth = config.get("depth", self._depth)


def process_with_protocol(
    image_path: str, output_path: str, filter_obj: ImageFilter
) -> None:
    print(f"\nUsing filter: {filter_obj.name}")
    image = Image.open(image_path)
    image = filter_obj.apply(image)
    image.save(output_path)
    print(f"Saved processed image to {output_path}")


# ----------- Main function -----------


def main() -> None:
    input_image: str = "input.jpg"  # Replace with a real image path

    # Protocol example
    sepia = SepiaFilter()
    sepia.configure({"depth": 15})
    process_with_protocol(input_image, "output_protocol_sepia.jpg", sepia)


if __name__ == "__main__":
    main()
