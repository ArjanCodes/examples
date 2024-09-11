import os

from bragir.constants import BLACKLISTED_FILES
from bragir.tracing.logger import logger


class NotAFileOrDirectoryError(Exception):
    pass


def get_files(path: str) -> list[str]:
    if os.path.isfile(path):
        return [path]
    if not os.path.isdir(path):
        raise NotAFileOrDirectoryError(f"{path} is not a file or directory")

    paths: list[str] = []

    for root, _dirs, nested_files in os.walk(path):
        for nested_file in nested_files:
            if nested_file not in BLACKLISTED_FILES:
                # Create the full path to the file
                logger.info(f"Adding file {nested_file} for translation")
                paths.append(os.path.join(root, nested_file))

    return paths
