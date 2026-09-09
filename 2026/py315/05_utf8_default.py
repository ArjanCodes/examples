"""PEP 686: omitted text-file encodings now default to UTF-8."""

from pathlib import Path
from tempfile import TemporaryDirectory


def main() -> None:
    message = "Python 3.15 says: café, 你好, 🚀"

    with TemporaryDirectory() as directory:
        path = Path(directory) / "greeting.txt"
        # No encoding= argument: Python 3.15 uses UTF-8 regardless of locale.
        path.write_text(message)
        print(path.read_text())

    print("For reusable applications, still specify encoding='utf-8' explicitly.")


if __name__ == "__main__":
    main()
