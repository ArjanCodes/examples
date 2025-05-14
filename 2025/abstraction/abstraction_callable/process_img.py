from typing import Callable

from PIL import Image

type ProcessFn = Callable[[image.Image], image.Image]


def process_img(image_path: str, output_path: str, filter_fn: ProcessFn) -> None:
    print(f"\nUsing filter: {filter_fn.__name__}")
    image = Image.open(image_path)
    image = filter_fn(image)
    image.save(output_path)
    print(f"Saved processed image to {output_path}")
