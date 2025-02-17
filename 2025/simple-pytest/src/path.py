import os

from src.constants.files import BLACKLISTED_FILES


def get_target_path(path: str, output: str) -> str:
    if output and os.path.isdir(output):
        root, _ = os.path.splitext(path)
        return os.path.join(output, os.path.basename(root) + ".srt")

    if output and os.path.isfile(output):
        return output

    root, _ = os.path.splitext(path)
    return root + ".srt"


def get_files(path: str) -> list[str]:
    paths: list[str] = []

    if os.path.isfile(path):
        return [path]

    for root, _dirs, nested_files in os.walk(path):
        for nested_file in nested_files:
            if nested_file not in BLACKLISTED_FILES:
                paths.append(os.path.join(root, nested_file))

    return paths
