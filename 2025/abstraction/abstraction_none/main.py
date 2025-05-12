from PIL import Image
from filters.grayscale import apply_grayscale
from filters.invert import apply_invert
from filters.sepia import apply_sepia


def main() -> None:
    image = Image.open("input.jpg")
    image = apply_grayscale(image)
    image = apply_invert(image)
    image = apply_sepia(image)

    image.save("output.jpg")
    print("Saved output.jpg")


if __name__ == "__main__":
    main()