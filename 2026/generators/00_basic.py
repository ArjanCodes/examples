from typing import Generator


def read_logs() -> Generator[str, None, None]:
    lines = [
        "info User logged in",
        "warning Slow database query",
        "error Payment failed",
    ]
    for line in lines:
        print(f"producing: {line}")
        yield line


def main():
    for line in read_logs():
        print(f"consuming: {line}")


if __name__ == "__main__":
    main()
