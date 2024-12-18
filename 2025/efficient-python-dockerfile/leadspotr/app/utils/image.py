import io

from fastapi import UploadFile
from PIL import Image

from ..db.schemas.image import Crop


def get_image_format(image: UploadFile) -> str:
    """Get image format.

    Args:
        image: Image to get format from.

    Returns:
        Image format.
    """

    return image.filename.split(".")[-1]


def crop_image(image: UploadFile, crop: Crop) -> bytes:
    """Crop image by crop box.

    Args:
        image: Image to crop.
        crop_box: Crop box.

    Returns:
        Cropped image.
    """

    # Read the uploaded image data
    image_data = image.file.read()

    # Open the image with PIL
    pil_image = Image.open(io.BytesIO(image_data))

    # Extract the crop coordinates
    x, y, width, height = crop.x, crop.y, crop.width, crop.height

    # Perform the image cropping
    cropped_image = pil_image.crop((x, y, x + width, y + height))

    # Create a new file-like object from the cropped image data
    cropped_image_data = io.BytesIO()
    cropped_image.save(cropped_image_data, format=get_image_format(image))

    return cropped_image_data.getvalue()
