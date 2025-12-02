# before_exitstack.py
from pathlib import Path


# BEFORE: deep nesting & manual cleanup
def read_files(paths: list[Path]) -> list[str]:
    results: list[str] = []
    for p in paths:
        if not p.exists():
            continue
        f = p.open()
        try:
            data = f.read()
            results.append(data)
        finally:
            f.close()
    return results


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
