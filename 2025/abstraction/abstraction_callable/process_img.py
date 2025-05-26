from typing import Callable

from PIL import Image

type ImageFilterFn = Callable[[Image], Image]


def process_img(image_path: str, output_path: str, filter_fn: ImageFilterFn) -> None:
    image = Image.open(image_path)
    image = filter_fn(image)
    image.save(output_path)
    print(f"Saved processed image to {output_path}")
