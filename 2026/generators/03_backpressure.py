import time
from dataclasses import dataclass
from enum import StrEnum, auto
from functools import reduce
from typing import Any, Callable, Generator, Iterable


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


# --- Pipeline stages ---
def parse_logs(lines: Iterable[str]) -> Generator[LogRecord, None, None]:
    for line in lines:
        print(f"parsing: {line}")
        level_text, message = line.split(" ", maxsplit=1)
        level = LogLevel(level_text)
        yield LogRecord(level=level, message=message)


def filter_important(
    records: Iterable[LogRecord],
) -> Generator[LogRecord, None, None]:
    for record in records:
        print(f"filtering: {record}")
        if record.level in {LogLevel.WARNING, LogLevel.ERROR}:
            yield record


def normalize_messages(
    records: Iterable[LogRecord],
) -> Generator[LogRecord, None, None]:
    for record in records:
        print(f"normalizing: {record}")
        yield LogRecord(
            level=record.level,
            message=record.message.lower(),
        )


# --- Composition helper ---
type PipelineStage = Callable[[Iterable[Any]], Iterable[Any]]


def compose(*stages: PipelineStage) -> PipelineStage:
    def apply(data: Iterable[Any]) -> Iterable[Any]:
        return reduce(lambda acc, stage: stage(acc), stages, data)

    return apply


# --- Slow consumer ---
def handle_records(records: Iterable[LogRecord]) -> None:
    for record in records:
        print(f"handling: {record}")
        time.sleep(1)


# --- Application entry point ---
def main() -> None:
    pipeline = compose(
        parse_logs,
        filter_important,
        normalize_messages,
    )

    handle_records(pipeline(read_logs()))


if __name__ == "__main__":
    main()
