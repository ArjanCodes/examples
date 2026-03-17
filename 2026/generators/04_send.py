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
        "warning Disk space low",
    ]
    for line in lines:
        print(f"producing: {line}")
        yield line


def parse_logs(lines: Iterable[str]) -> Generator[LogRecord, None, None]:
    for line in lines:
        level_text, message = line.split(" ", maxsplit=1)
        yield LogRecord(level=LogLevel(level_text), message=message)


def should_emit(record: LogRecord, threshold: LogLevel) -> bool:
    if threshold is LogLevel.WARNING:
        return record.level in {LogLevel.WARNING, LogLevel.ERROR}
    return record.level is LogLevel.ERROR


# --- Simpler send() example ---
def threshold_filter() -> Generator[LogLevel, LogLevel | None, None]:
    threshold = LogLevel.ERROR
    while True:
        new_threshold = yield threshold
        if new_threshold is not None:
            threshold = new_threshold


def main() -> None:
    records = parse_logs(read_logs())

    filter_settings = threshold_filter()
    threshold = next(filter_settings)  # prime the generator

    for index, record in enumerate(records):
        if index == 2:
            threshold = filter_settings.send(LogLevel.WARNING)
        else:
            threshold = next(filter_settings)

        if should_emit(record, threshold):
            print(f"handling: {record}")


if __name__ == "__main__":
    main()
