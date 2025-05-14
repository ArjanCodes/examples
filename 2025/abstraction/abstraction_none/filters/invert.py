from PIL import Image, ImageOps


class InvertFilter:
    @property
    def name(self) -> str:
        return "Invert"

    def do_invert(self, image: Image.Image) -> Image.Image:
        print(f"Applying {self.name} filter")
        return ImageOps.invert(image.convert("RGB"))
