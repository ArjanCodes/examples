import os


def get_target_path(path: str, output: str) -> str:
    if output and os.path.isdir(output):
        root, _ = os.path.splitext(path)
        return os.path.join(output, os.path.basename(root) + ".srt")

    if output and os.path.isfile(output):
        return output

    root, _ = os.path.splitext(path)
    return root + ".srt"
