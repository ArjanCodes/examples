from typing import Any, Protocol

from PIL import Image


class FilterBase(Protocol):
    @property
    def name(self) -> str: ...

    def apply(self, image: Image.Image) -> Image.Image: ...

    def configure(self, config: dict[str, Any]) -> None: ...


def process_img(image_path: str, output_path: str, filter_obj: FilterBase) -> None:
    print(f"\nUsing filter: {filter_obj.name}")
    image = Image.open(image_path)
    image = filter_obj.apply(image)
    image.save(output_path)
    print(f"Saved processed image to {output_path}")
