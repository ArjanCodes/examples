from typing import Any
from process_img import process_with_abc
from filters.grayscale import GrayscaleFilter
from filters.invert import InvertFilter


def main() -> None:
    input_image: str = "../input.jpg"

    grayscale = GrayscaleFilter()
    grayscale.configure({"intensity": 0.8})
    process_with_abc(input_image, "output_abc_grayscale.jpg", grayscale)

    invert = InvertFilter()
    invert.configure({"enabled": True})
    process_with_abc(input_image, "output_abc_invert.jpg", invert)


if __name__ == "__main__":
    main()
