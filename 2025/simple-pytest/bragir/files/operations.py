def read_file(file_path: str):
    with open(file=file_path, mode="r") as file:
        file_content = file.read()
    return file_content


def create_file(file_path: str, content: str):
    with open(file=file_path, mode="w", encoding="utf-8") as fileIO:
        fileIO.write(content)
