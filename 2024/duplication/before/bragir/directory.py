import os

from bragir.constants import BLACKLISTED_FILES
from bragir.tracing.logger import logger


def get_files_in_directory(path: str) -> list[str]:
    paths: list[str] = []

    for root, _dirs, nested_files in os.walk(path):
        for nested_file in nested_files:
            if nested_file not in BLACKLISTED_FILES:
                # Create the full path to the file
                logger.info(f"Adding file {nested_file} for translation")
                paths.append(os.path.join(root, nested_file))

    return paths
