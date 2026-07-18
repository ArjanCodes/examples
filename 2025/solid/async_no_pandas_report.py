"""
===============================================================================
Sales Report - True Async Streaming Implementation
===============================================================================
Fully asynchronous, non-blocking reporting pipeline:
    * Reads CSV line by line using aiofiles (no pandas blocking)
    * Parses each record asynchronously using csv.DictReader
    * Aggregates metrics incrementally (no in-memory dataset)
    * Writes JSON output asynchronously

This version is a true example of async I/O — no fake async via thread executors.
Perfect for large files or integration into larger async systems.
===============================================================================
"""

import aiofiles
import asyncio
import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

# ------------------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [async-true] %(message)s",
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
OUTPUT_FILE = OUTPUT_DIR / "sales_report_async_true.json"
REPORT_START = datetime(2024, 1, 1)
REPORT_END = datetime(2024, 12, 31)


# ------------------------------------------------------------------------------
# Async Data Processing
# ------------------------------------------------------------------------------


async def parse_and_aggregate_csv(
    file_path: Path,
    start: datetime | None = None,
    end: datetime | None = None,
) -> dict[str, Any]:
    """
    Asynchronously reads and aggregates sales data.
    Computes metrics incrementally to avoid loading entire file in memory.
    """

    num_customers: set[str] = set()
    total_sales = 0.0
    positive_sales: list[float] = []
    total_records = 0
    total_returns = 0

    logger.info("Reading asynchronously from %s", file_path)

    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as afp:
        # Read header line for DictReader initialization
        header_line = await afp.readline()
        headers = header_line.strip().split(",")
        reader = csv.DictReader([],
                                fieldnames=[h.strip('"') for h in headers])

        # Process line by line
        async for line in afp:
            if not line.strip():
                continue

            values = list(csv.reader([line]))[0]
            record = dict(zip(reader.fieldnames, values))

            try:
                sale_date = datetime.fromisoformat(record["date"].strip('"'))
                price = float(record["price"])
                name = record["name"].strip('"')
            except Exception:
                # Skip badly formed lines safely
                continue

            if start and sale_date < start or end and sale_date > end:
                continue

            total_records += 1
            num_customers.add(name)
            total_sales += price

            if price > 0:
                positive_sales.append(price)
            elif price < 0:
                total_returns += 1

    avg_order_value = sum(positive_sales) / len(positive_sales) if positive_sales else 0.0
    percentage_returns = (
        (total_returns / total_records) * 100 if total_records else 0.0
    )

    logger.info(
        "Processed %d records (%d customers, %.2f avg order)",
        total_records,
        len(num_customers),
        avg_order_value,
    )

    return {
        "number_of_customers": len(num_customers),
        "average_order_value (pre-tax)": round(avg_order_value, 2),
        "percentage_of_returns": round(percentage_returns, 2),
        "total_sales_in_period (pre-tax)": round(total_sales, 2),
        "report_start": start.strftime("%Y-%m-%d") if start else "N/A",
        "report_end": end.strftime("%Y-%m-%d") if end else "N/A",
    }


async def write_report(report: dict[str, Any], file_path: Path) -> None:
    """Writes the computed report asynchronously to JSON."""

    async with aiofiles.open(file_path, mode="w", encoding="utf-8") as afp:
        await afp.write(json.dumps(report, indent=2))
    logger.info("Async streaming report written to %s", file_path)


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------


async def main() -> None:
    logger.info("Starting true asynchronous sales report pipeline...")

    try:
        report_data = await parse_and_aggregate_csv(
            INPUT_FILE, REPORT_START, REPORT_END
        )
        await write_report(report_data, OUTPUT_FILE)
        logger.info("Report generation completed successfully.")
    except Exception as exc:
        logger.exception("Async streaming report failed: %s", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    asyncio.run(main())