def process(data: str) -> None:
    print("Processing data")


def main() -> None:
    file = None
    try:
        file = open("data.txt", "r")
        data = file.read()
    except IOError:
        print("Error reading file")
    else:
        # Process the data
        process(data)
    finally:
        if file is not None:
            file.close()
