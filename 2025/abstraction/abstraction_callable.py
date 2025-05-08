from typing import Callable

from PIL import Image, ImageOps

type ImageFilterFunc = Callable[[Image.Image], Image.Image]


def make_grayscale_filter(intensity: float = 1.0) -> ImageFilterFunc:
    def filter_func(image: Image.Image) -> Image.Image:
        print(f"Applying grayscale filter with intensity {intensity}")
        # Note: intensity isn't actually used by Pillow here, but it demonstrates config
        return ImageOps.grayscale(image)

    return filter_func


def make_invert_filter(enabled: bool = True) -> ImageFilterFunc:
    def filter_func(image: Image.Image) -> Image.Image:
        if enabled:
            print("Applying invert filter")
            return ImageOps.invert(image.convert("RGB"))
        else:
            print("Invert filter disabled, returning original image")
            return image

    return filter_func


def make_sepia_filter(depth: int = 20) -> ImageFilterFunc:
    def filter_func(image: Image.Image) -> Image.Image:
        print(f"Applying sepia filter with depth {depth}")
        sepia_image = image.convert("RGB")
        width, height = sepia_image.size
        pixels = sepia_image.load()

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b + depth)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b + depth)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b + depth)
                pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))
        return sepia_image

    return filter_func


def process_image(
    image_path: str, output_path: str, filter_func: ImageFilterFunc, filter_name: str
) -> None:
    print(f"\nUsing filter: {filter_name}")
    image = Image.open(image_path)
    image = filter_func(image)
    image.save(output_path)
    print(f"Saved processed image to {output_path}")


def main() -> None:
    input_image: str = "input.jpg"

    # Create configured filters
    grayscale_filter = make_grayscale_filter(intensity=0.8)
    invert_filter = make_invert_filter(enabled=True)
    sepia_filter = make_sepia_filter(depth=15)

    # Apply filters
    process_image(
        input_image, "output_callable_grayscale.jpg", grayscale_filter, "Grayscale"
    )
    process_image(input_image, "output_callable_invert.jpg", invert_filter, "Invert")
    process_image(input_image, "output_callable_sepia.jpg", sepia_filter, "Sepia")


if __name__ == "__main__":
    main()
