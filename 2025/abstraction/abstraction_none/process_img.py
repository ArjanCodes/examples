from typing import Any

from filters.grayscale import GrayscaleFilter
from filters.invert import InvertFilter
from PIL import Image


def process_img(image_path: str, output_path: str, filter_obj: Any) -> None:
    print(f"\nUsing filter: {filter_obj.name}")
    image = Image.open(image_path)
    if isinstance(filter_obj, GrayscaleFilter):
        filter_obj.configure({"intensity": 0.8})
        image = filter_obj.apply(image)
    elif isinstance(filter_obj, InvertFilter):
        image = filter_obj.do_invert(image)
    else:
        print("Unknown filter type. Skipping configuration.")

    image.save(output_path)
    print(f"Saved processed image to {output_path}")
