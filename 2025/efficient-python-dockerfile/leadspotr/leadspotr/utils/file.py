import base64
from uuid import uuid4

from google.cloud.storage import Blob, Client

from ..config import settings
from ..utils.logger import logger


def encode_file_to_base64(file_path: str) -> str:
    """
    Encodes a file to base64 string.
    """
    with open(file_path, "rb") as f:
        file = f.read()
        f.close()
    encoded_file = base64.b64encode(file).decode("utf-8")

    return encoded_file


def create_file_url(file_name: str | None, folder_name: str, content_type: str) -> str:
    """
    Creates a file url from a given file name and folder name.
    """

    if not file_name:
        return f"{folder_name}/{uuid4()}.{content_type.split('/')[1]}"

    return f"{folder_name}/{file_name}.{content_type.split('/')[1]}"


def upload_file(file_data: bytes, content_type: str, folder_name: str) -> str:
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """

    file_url = create_file_url(
        file_name=str(uuid4()), folder_name=folder_name, content_type=content_type
    )

    blob = construct_blob(file_url)
    blob.upload_from_string(data=file_data, content_type=content_type)  # type: ignore

    logger.info("Uploaded %s to %s bucket", file_url, settings.GOOGLE_STORAGE_BUCKET)

    return blob.public_url


def delete_uploaded_file(file_url: str) -> str:
    """
    Deletes a file from a given Cloud Storage bucket.
    """
    blob = construct_blob(file_url)

    blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
    generation_match_precondition = blob.generation

    blob.delete(if_generation_match=generation_match_precondition)
    logger.info("Deleted %s from %s bucket", blob.name, settings.GOOGLE_STORAGE_BUCKET)

    return blob.public_url


def construct_blob(file_url: str) -> Blob:
    """
    Constructs a Blob object from a given file url.
    """
    bucketname = settings.GOOGLE_STORAGE_BUCKET

    client = Client()
    bucket = client.bucket(bucketname)

    file_name_parts = file_url.split("/")
    filename = file_name_parts[-2] + "/" + file_name_parts[-1]

    return bucket.blob(filename)
