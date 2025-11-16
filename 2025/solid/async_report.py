"""
===============================================================================
Sales Report - Asynchronous Implementation
===============================================================================
Uses asyncio to concurrently compute metrics and handle async I/O operations.

Highlights:
    * Concurrent execution of metric computations
    * Async-friendly structure (could be extended for DB/API operations)
===============================================================================
"""

import asyncio
import json
import logging
from collections.abc import Awaitable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import aiofiles  # Async file I/O
import pandas as pd

# ------------------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [async] %(message)s",
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
OUTPUT_FILE = OUTPUT_DIR / "sales_report_async.json"
REPORT_START = datetime(2024, 1, 1)
REPORT_END = datetime(2024, 12, 31)

# ------------------------------------------------------------------------------
# Data and Config
# ------------------------------------------------------------------------------


@dataclass
class ReportConfig:
    """Configuration for asynchronous report generation."""

    input_file: Path
    output_file: Path
    start_date: datetime | None = None
    end_date: datetime | None = None


# ------------------------------------------------------------------------------
# Async Helpers
# ------------------------------------------------------------------------------


async def read_sales(file: Path) -> pd.DataFrame:
    """Simulates asynchronous file read (e.g., using aiofiles or async API)."""
    logger.info("Reading data asynchronously from %s", file)
    # Pandas isn't async, but this placeholder represents async I/O in real case
    loop = asyncio.get_running_loop()
    df = await loop.run_in_executor(None, lambda: pd.read_csv(file, parse_dates=["date"]))  # pyright: ignore[reportUnknownMemberType]
    logger.info("Data loaded successfully: %d rows", len(df))
    return df


async def filter_sales(
    df: pd.DataFrame, start: datetime | None, end: datetime | None
) -> pd.DataFrame:
    """Filters sales asynchronously by date range."""

    loop = asyncio.get_running_loop()

    def _filter() -> pd.DataFrame:
        filtered = df
        if start:
            filtered = filtered.loc[filtered["date"] >= pd.Timestamp(start)]
        if end:
            filtered = filtered.loc[filtered["date"] <= pd.Timestamp(end)]
        return filtered

    result = await loop.run_in_executor(None, _filter)
    logger.info("Filtered dataset to %d records", len(result))
    return result


# ------------------------------------------------------------------------------
# Async Metric Coroutines
# ------------------------------------------------------------------------------


async def customer_count_metric(df: pd.DataFrame) -> dict[str, Any]:
    await asyncio.sleep(0.01)
    return {"number_of_customers": df["name"].nunique()}


async def average_order_value_metric(df: pd.DataFrame) -> dict[str, Any]:
    await asyncio.sleep(0.01)
    positive_sales = df[df["price"] > 0]["price"]
    avg = positive_sales.mean() if not positive_sales.empty else 0.0
    return {"average_order_value (pre-tax)": round(avg, 2)}


async def return_percentage_metric(df: pd.DataFrame) -> dict[str, Any]:
    await asyncio.sleep(0.01)
    returns = df[df["price"] < 0]
    pct = (len(returns) / len(df)) * 100 if len(df) else 0.0
    return {"percentage_of_returns": round(pct, 2)}


async def total_sales_metric(df: pd.DataFrame) -> dict[str, Any]:
    await asyncio.sleep(0.01)
    return {"total_sales_in_period (pre-tax)": round(df["price"].sum(), 2)}


# ------------------------------------------------------------------------------
# Report Assembly
# ------------------------------------------------------------------------------


async def compute_metrics(
    df: pd.DataFrame, start: datetime | None, end: datetime | None
) -> dict[str, Any]:
    """Runs metric computations concurrently using asyncio.gather()."""

    logger.info("Computing metrics concurrently...")
    tasks: list[Awaitable[dict[str, Any]]] = [
        customer_count_metric(df),
        average_order_value_metric(df),
        return_percentage_metric(df),
        total_sales_metric(df),
    ]
    results = await asyncio.gather(*tasks)

    report: dict[str, Any] = {}
    for r in results:
        report |= r

    report["report_start"] = start.strftime("%Y-%m-%d") if start else "N/A"
    report["report_end"] = end.strftime("%Y-%m-%d") if end else "N/A"

    return report


async def write_report(report: dict[str, Any], path: Path) -> None:
    """Asynchronously writes JSON report to file."""
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(report, indent=2))
    logger.info("Async report written to: %s", path)


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------


async def main() -> None:
    config = ReportConfig(
        input_file=INPUT_FILE,
        output_file=OUTPUT_FILE,
        start_date=REPORT_START,
        end_date=REPORT_END,
    )

    try:
        df = await read_sales(config.input_file)
        filtered_df = await filter_sales(df, config.start_date, config.end_date)
        report = await compute_metrics(filtered_df, config.start_date, config.end_date)
        await write_report(report, config.output_file)
        logger.info("Async report generation completed successfully.")
    except Exception as e:
        logger.exception("Failed during async report generation: %s", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    asyncio.run(main())
