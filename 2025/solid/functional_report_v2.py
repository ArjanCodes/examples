"""
===============================================================================
Sales Report - Functional Implementation
===============================================================================
A lightweight, flat functional approach to compute and write a
sales performance report.

Structure:
    * "Pure" functions for reading, filtering, and metrics
    * Simple data flow: read → filter → compute → write
===============================================================================
"""

import json
import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

# ------------------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
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
OUTPUT_FILE = OUTPUT_DIR / "sales_report_functional.json"
REPORT_START = datetime(2024, 1, 1)
REPORT_END = datetime(2024, 12, 31)

# ------------------------------------------------------------------------------
# Type aliases and config
# ------------------------------------------------------------------------------

type MetricFn = Callable[[pd.DataFrame], dict[str, Any]]


@dataclass
class ReportConfig:
    """Encapsulates configuration for the functional report process."""

    input_file: Path
    start_date: datetime | None = None
    end_date: datetime | None = None
    metrics: list[MetricFn] = field(default_factory=list)


# ------------------------------------------------------------------------------
# Functional Components
# ------------------------------------------------------------------------------


def read_sales(file: Path) -> pd.DataFrame:
    """Reads the sales CSV data into a pandas DataFrame."""

    logger.info("Reading data from %s", file)
    return pd.read_csv(file, parse_dates=["date"])  # pyright: ignore[reportUnknownMemberType]


def filter_sales(df: pd.DataFrame, start: datetime | None, end: datetime | None) -> pd.DataFrame:
    """Applies optional start/end-date filters to the dataframe."""

    if start:
        df = df[df["date"] >= pd.Timestamp(start)]
    if end:
        df = df[df["date"] <= pd.Timestamp(end)]

    logger.info("Filtered dataset contains %d records", len(df))
    return df


# ------------------------------------------------------------------------------
# Metrics Functions
# ------------------------------------------------------------------------------


def customer_count_metric(df: pd.DataFrame) -> dict[str, Any]:
    """Counts distinct customers."""

    return {"number_of_customers": df["name"].nunique()}


def average_order_value_metric(df: pd.DataFrame) -> dict[str, Any]:
    """Computes the average value of positive (non-return) transactions."""

    sales = df[df["price"] > 0]["price"]
    avg = sales.mean() if not sales.empty else 0.0
    return {"average_order_value (pre-tax)": round(avg, 2)}


def return_percentage_metric(df: pd.DataFrame) -> dict[str, Any]:
    """Calculates the percentage of rows representing returns."""

    returns = df[df["price"] < 0]
    pct = (len(returns) / len(df)) * 100 if len(df) > 0 else 0
    return {"percentage_of_returns": round(pct, 2)}


def total_sales_metric(df: pd.DataFrame) -> dict[str, Any]:
    """Computes total sales before tax."""

    return {"total_sales_in_period (pre-tax)": round(df["price"].sum(), 2)}


# ------------------------------------------------------------------------------
# Reporting Pipeline
# ------------------------------------------------------------------------------


def generate_report_data(df: pd.DataFrame, config: ReportConfig) -> dict[str, Any]:
    """Executes all metrics and produces a report dictionary."""

    logger.info("Computing metrics...")
    result: dict[str, Any] = {}
    for metric in config.metrics:
        result.update(metric(df))
    result["report_start"] = config.start_date.strftime("%Y-%m-%d") if config.start_date else "N/A"
    result["report_end"] = config.end_date.strftime("%Y-%m-%d") if config.end_date else "N/A"

    logger.info("Metrics computed successfully.")
    return result


def write_report(data: dict[str, Any], file: Path) -> None:
    """Writes the final report JSON to disk."""

    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    logger.info("Report written to %s", file)


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------


def main() -> None:
    """Runs the full functional data pipeline."""

    config = ReportConfig(
        input_file=INPUT_FILE,
        start_date=REPORT_START,
        end_date=REPORT_END,
        metrics=[
            customer_count_metric,
            average_order_value_metric,
            return_percentage_metric,
            total_sales_metric,
        ],
    )

    try:
        df = read_sales(config.input_file)
        df = filter_sales(df, config.start_date, config.end_date)
        report = generate_report_data(df, config)
        write_report(report, OUTPUT_FILE)
    except Exception as e:
        logger.exception("Failed to generate report: %s", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
