from collections.abc import Generator, Iterable
from dataclasses import dataclass
from enum import StrEnum, auto


class LogLevel(StrEnum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


@dataclass(slots=True)
class LogRecord:
    level: LogLevel
    message: str


def read_logs() -> Generator[str, None, None]:
    lines = [
        "info User logged in",
        "warning Slow database query",
        "error Payment failed",
    ]
    for line in lines:
        yield line


def parse_logs(lines: Iterable[str]) -> Generator[LogRecord, None, int]:
    count = 0
    for line in lines:
        level_text, message = line.split(" ", maxsplit=1)
        yield LogRecord(level=LogLevel(level_text), message=message)
        count += 1

    return count  # 👈 final result


def main() -> None:
    parser = parse_logs(read_logs())

    try:
        while True:
            record = next(parser)
            print(f"handling: {record}")
    except StopIteration as e:
        print(f"Total records processed: {e.value}")


if __name__ == "__main__":
    main()
