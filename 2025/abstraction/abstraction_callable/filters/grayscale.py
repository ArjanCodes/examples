from PIL import Image, ImageOps


def apply_grayscale(image: Image.Image, intensity: float) -> Image.Image:
    print(f"Applying grayscale filter with intensity {intensity}")
        grayscale_image = ImageOps.grayscale(image)
        if intensity < 1.0:
            return Image.blend(image, grayscale_image, intensity)
        return grayscale_image
