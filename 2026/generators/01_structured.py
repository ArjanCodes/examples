from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Generator, Iterable


# --- Domain model ---
class LogLevel(StrEnum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


@dataclass(slots=True)
class LogRecord:
    level: LogLevel
    message: str


# --- Source generator ---
def read_logs() -> Generator[str, None, None]:
    lines = [
        "info User logged in",
        "warning Slow database query",
        "error Payment failed",
    ]
    for line in lines:
        print(f"producing: {line}")
        yield line


# --- Transformation step ---
def parse_logs(lines: Iterable[str]) -> Generator[LogRecord, None, None]:
    for line in lines:
        level_text, message = line.split(" ", maxsplit=1)
        level = LogLevel(level_text)  # validated conversion
        yield LogRecord(level=level, message=message)


def handle_records(records: Iterable[LogRecord]) -> None:
    for record in records:
        print(f"handling: {record}")


# --- Application entry point ---
def main() -> None:
    records = parse_logs(read_logs())
    handle_records(records)


if __name__ == "__main__":
    main()
