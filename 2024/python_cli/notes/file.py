import os

from config import load_config


def create_files(pattern: str, start: int = 0, end: int = 10) -> list[str]:
    config = load_config()
    notes_dir = config.get("notes_dir")

    if notes_dir is None:
        raise ValueError("Notes directory not configured.")

    base_name, extension = pattern.split("*")
    extension = extension.lstrip(".")

    files: list[str] = []
    for i in range(start, end + 1):
        file_name = f"{base_name}{i}.{extension}"

        if exists(file_name):
            continue

        with open(os.path.join(notes_dir, file_name), "w") as file:
            file.write(f"This is the content of {file_name}\n")
        files.append(file_name)

    return files


def load(path: str):
    config = load_config()
    notes_dir = config.get("notes_dir")

    if notes_dir is None:
        raise ValueError("Notes directory not configured.")

    with open(os.path.join(notes_dir, path), "r") as file:
        return file.read()


def save(path: str, content: str):
    config = load_config()
    notes_dir = config.get("notes_dir")

    if notes_dir is None:
        raise ValueError("Notes directory not configured.")
    with open(os.path.join(notes_dir, path), "w+") as file:
        file.write(content)


def exists(path: str):
    config = load_config()
    notes_dir = config.get("notes_dir")

    if notes_dir is None:
        raise ValueError("Notes directory not configured.")
    return os.path.isfile(os.path.join(notes_dir, path))
