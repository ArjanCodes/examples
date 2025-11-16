"""
===============================================================================
Sales Report - Actor Model Implementation
===============================================================================
Implements the report workflow using the Actor Model:
    * Each actor runs concurrently and communicates via message passing.
    * Actors never share state; they exchange messages through asyncio queues.
    * Demonstrates isolated concurrency with cooperative scheduling.

Actors:
    - ReaderActor  : Reads CSV rows asynchronously
    - FilterActor  : Filters rows by date range
    - MetricsActor : Computes aggregate metrics incrementally
    - WriterActor  : Writes final report to disk

Highlights:
    * Concurrency through message passing (no shared memory)
    * Fault isolation between components
    * Natural fit for distributed or reactive architectures
===============================================================================
"""

import asyncio
import csv
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import aiofiles

# ------------------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [actor] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "sales_data.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "sales_report_actor.json"
REPORT_START_DATE = datetime(2024, 1, 1)
REPORT_END_DATE = datetime(2024, 12, 31)

# ------------------------------------------------------------------------------
# Actor Base Class
# ------------------------------------------------------------------------------


class Actor:
    """Base actor defining inbox and cooperative message loop."""

    def __init__(self, name: str):
        self.name = name
        self.inbox: asyncio.Queue[Any] = asyncio.Queue()
        self._task: asyncio.Task[Any] | None = None

    async def send(self, message: Any) -> None:
        """Send a message to this actor's inbox."""
        await self.inbox.put(message)

    async def handle(self, message: Any) -> None:
        """Override in subclasses to define message behavior."""
        raise NotImplementedError

    async def run(self) -> None:
        """Continuously process messages until STOP signal."""
        logger.info("%s started.", self.name)
        while True:
            message = await self.inbox.get()
            if message == "STOP":
                logger.info("%s stopped.", self.name)
                return
            try:
                await self.handle(message)
            except Exception as exc:
                logger.exception("[%s] Error handling message: %s", self.name, exc)

    def start(self) -> None:
        """Launch the actor event loop in background."""
        self._task = asyncio.create_task(self.run(), name=f"{self.name}-task")

    async def stop(self) -> None:
        """Send stop signal and await task completion."""
        await self.send("STOP")
        if self._task:
            await self._task


# ------------------------------------------------------------------------------
# Domain Structures
# ------------------------------------------------------------------------------

@dataclass
class SalesRecord:
    name: str
    date: datetime
    price: float


# ------------------------------------------------------------------------------
# Actor Implementations
# ------------------------------------------------------------------------------


class ReaderActor(Actor):
    """Reads CSV rows and sends them downstream."""

    def __init__(self, name: str, file_path: Path, next_actor: Actor):
        super().__init__(name)
        self.file_path = file_path
        self.next_actor = next_actor

    async def handle(self, _: Any) -> None:
        logger.info("[%s] Reading file: %s", self.name, self.file_path)
        async with aiofiles.open(self.file_path, "r", encoding="utf-8") as afp:
            header_line = await afp.readline()
            headers = [h.strip('"') for h in header_line.strip().split(",")]
            reader = csv.DictReader([], fieldnames=headers)

            async for line in afp:
                values = next(csv.reader([line]))
                row = dict(zip(reader.fieldnames, values))
                try:
                    record = SalesRecord(
                        name=row["name"].strip('"'),
                        date=datetime.fromisoformat(row["date"].strip('"')),
                        price=float(row["price"]),
                    )
                    await self.next_actor.send(record)
                except Exception as exc:
                    logger.warning("[%s] Skipping malformed row: %s (%s)", self.name, row, exc)

        await self.next_actor.send("EOF")


class FilterActor(Actor):
    """Filters records that fall outside a date range."""

    def __init__(self, name: str, start_date: datetime, end_date: datetime, next_actor: Actor):
        super().__init__(name)
        self.start_date = start_date
        self.end_date = end_date
        self.next_actor = next_actor

    async def handle(self, message: Any) -> None:
        if message == "EOF":
            await self.next_actor.send("EOF")
            return
        record: SalesRecord = message
        if self.start_date <= record.date <= self.end_date:
            await self.next_actor.send(record)


class MetricsActor(Actor):
    """Accumulates sales metrics incrementally."""

    def __init__(self, name: str, next_actor: Actor):
        super().__init__(name)
        self.next_actor = next_actor
        self.num_customers: set[str] = set()
        self.positive_prices: list[float] = []
        self.returns_count: int = 0
        self.total_records: int = 0
        self.total_sales: float = 0.0

    async def handle(self, message: Any) -> None:
        if message == "EOF":
            await self._finalize()
            await self.next_actor.send("EOF")
            return

        record: SalesRecord = message
        self.total_records += 1
        self.num_customers.add(record.name)
        self.total_sales += record.price

        if record.price > 0:
            self.positive_prices.append(record.price)
        elif record.price < 0:
            self.returns_count += 1

    async def _finalize(self) -> None:
        avg_order_value = (
            sum(self.positive_prices) / len(self.positive_prices)
            if self.positive_prices
            else 0.0
        )
        pct_returns = (
            (self.returns_count / self.total_records) * 100 if self.total_records else 0.0
        )
        report = {
            "number_of_customers": len(self.num_customers),
            "average_order_value (pre-tax)": round(avg_order_value, 2),
            "percentage_of_returns": round(pct_returns, 2),
            "total_sales_in_period (pre-tax)": round(self.total_sales, 2),
            "report_start": REPORT_START_DATE.strftime("%Y-%m-%d"),
            "report_end": REPORT_END_DATE.strftime("%Y-%m-%d"),
        }
        logger.info("[%s] Metrics computed. Forwarding to writer...", self.name)
        await self.next_actor.send(report)


class WriterActor(Actor):
    """Receives final report and writes it to disk."""

    def __init__(self, name: str, output_file: Path):
        super().__init__(name)
        self.output_file = output_file

    async def handle(self, message: Any) -> None:
        if message == "EOF":
            # Writer receives EOF last—it can stop silently
            return
        report: dict[str, Any] = message
        await asyncio.to_thread(self._write_json, report)
        logger.info("[%s] Report successfully written to %s", self.name, self.output_file)

    def _write_json(self, report: dict[str, Any]) -> None:
        self.output_file.write_text(json.dumps(report, indent=2), encoding="utf-8")


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------


async def main() -> None:
    """Assemble and execute the concurrent actor system."""

    logger.info("Starting Actor Model Sales Report...")

    # Instantiate the actor chain
    writer = WriterActor("WriterActor", OUTPUT_FILE)
    metrics = MetricsActor("MetricsActor", next_actor=writer)
    filterer = FilterActor("FilterActor", REPORT_START_DATE, REPORT_END_DATE, next_actor=metrics)
    reader = ReaderActor("ReaderActor", INPUT_FILE, next_actor=filterer)

    actors = [reader, filterer, metrics, writer]

    # Start all actors
    for a in actors:
        a.start()

    # Kick off processing
    await reader.send("START")

    # Wait for all to gracefully shut down
    for a in actors:
        await a.stop()

    logger.info("Actor Model Sales Report completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())