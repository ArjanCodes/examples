from PIL import Image
from filters.base import FilterBase

def process_with_abc(image_path: str, output_path: str, filter_obj: FilterBase) -> None:
    print(f"\nUsing filter: {filter_obj.name}")
    image = Image.open(image_path)
    image = filter_obj.apply(image)
    image.save(output_path)
    print(f"Saved processed image to {output_path}")