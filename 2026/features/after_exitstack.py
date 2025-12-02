from contextlib import ExitStack
from pathlib import Path


def read_files(paths: list[Path]) -> list[str]:
    with ExitStack() as stack:
        files = [stack.enter_context(p.open()) for p in paths if p.exists()]
        return [f.read() for f in files]


def main():
    p1 = Path("file1.txt")
    p2 = Path("file2.txt")
    p1.write_text("Hello!")
    p2.write_text("World!")

    print(read_files([p1, p2]))

    p1.unlink()
    p2.unlink()


if __name__ == "__main__":
    main()
