from pathlib import Path

def rename_jpegs(folder: str):
    for file in Path(folder).glob("*.jpeg"):
        file.rename(file.with_suffix(".jpg"))