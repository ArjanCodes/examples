from functools import partial

from filters.grayscale import apply_grayscale
from filters.invert import apply_invert
from PIL import Image, ImageOps
from process_img import process_img


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


def main() -> None:
    input_image: str = "../input.jpg"

    grayscale_fn = partial(apply_grayscale, intensity=0.8)
    process_img(input_image, "output_abc_grayscale.jpg", grayscale_fn)

    process_img(input_image, "output_abc_invert.jpg", apply_invert)


if __name__ == "__main__":
    main()
