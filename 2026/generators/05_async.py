import asyncio
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import AsyncGenerator


# --- Domain model ---
class LogLevel(StrEnum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


@dataclass(slots=True)
class LogRecord:
    level: LogLevel
    message: str


# --- Async source generator ---
async def read_logs() -> AsyncGenerator[str, None]:
    lines = [
        "info User logged in",
        "warning Slow database query",
        "error Payment failed",
    ]
    for line in lines:
        await asyncio.sleep(0.5)
        print(f"producing: {line}")
        yield line


# --- Async pipeline stages ---
async def parse_logs(
    lines: AsyncGenerator[str, None],
) -> AsyncGenerator[LogRecord, None]:
    async for line in lines:
        print(f"parsing: {line}")
        level_text, message = line.split(" ", maxsplit=1)
        level = LogLevel(level_text)
        yield LogRecord(level=level, message=message)


async def filter_important(
    records: AsyncGenerator[LogRecord, None],
) -> AsyncGenerator[LogRecord, None]:
    async for record in records:
        print(f"filtering: {record}")
        if record.level in {LogLevel.WARNING, LogLevel.ERROR}:
            yield record


async def normalize_messages(
    records: AsyncGenerator[LogRecord, None],
) -> AsyncGenerator[LogRecord, None]:
    async for record in records:
        print(f"normalizing: {record}")
        yield LogRecord(
            level=record.level,
            message=record.message.lower(),
        )


# --- Consumer ---
async def handle_records(records: AsyncGenerator[LogRecord, None]) -> None:
    async for record in records:
        print(f"handling: {record}")
        await asyncio.sleep(1)


# --- Application entry point ---
async def main() -> None:
    records = read_logs()
    parsed = parse_logs(records)
    filtered = filter_important(parsed)
    normalized = normalize_messages(filtered)

    await handle_records(normalized)


if __name__ == "__main__":
    asyncio.run(main())
