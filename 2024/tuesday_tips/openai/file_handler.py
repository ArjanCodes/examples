def read_file(filename: str) -> str:
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."
    except IOError:
        return "An error occurred while reading the file."
