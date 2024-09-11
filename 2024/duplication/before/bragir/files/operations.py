from bragir.files.file import File
from bragir.tracing.logger import logger


def read_file(file_path: str):
    with open(file_path, "r") as file:
        file_content = file.read()
    return file_content


def create_file(file: File, content: str):
    logger.info(f"Creating file {file.target_path}")
    with open(file.target_path, "a+", encoding="utf-8") as fileIO:
        fileIO.write(content)
        logger.info(f"Created file {file.target_path}")
