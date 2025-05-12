from PIL import Image, ImageOps


def apply_grayscale(image: Image.Image) -> Image.Image:
    print("Applying grayscale filter")
    return ImageOps.grayscale(image)