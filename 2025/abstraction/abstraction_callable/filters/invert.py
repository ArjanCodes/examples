from PIL import Image, ImageOps


def apply_invert(image: Image.Image) -> Image.Image:
    print("Applying invert filter")
    return ImageOps.invert(image.convert("RGB"))