"""
===============================================================================
Sales Report - Class-Based Implementation
===============================================================================
Generates a summarized sales performance report using an object-oriented (OOP)
approach that follows SOLID principles.

Structure:
    * CsvSalesReader - Responsible for reading raw CSV data.
    * DateRangeFilter - Handles date range filtering.
    * Metric classes - Each computes a single metric.
    * SalesReportGenerator - Coordinates the workflow.
    * JSONReportWriter - Persists report results to JSON.
===============================================================================
"""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol

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
OUTPUT_FILE = OUTPUT_DIR / "sales_report_class.json"
REPORT_START = datetime(2024, 1, 1)
REPORT_END = datetime(2024, 12, 31)

# ------------------------------------------------------------------------------
# Config and Protocols
# ------------------------------------------------------------------------------


@dataclass
class ReportConfig:
    """Configuration object controlling report generation parameters."""

    input_file: Path
    output_file: Path
    start_date: datetime | None = None
    end_date: datetime | None = None


class SalesReader(Protocol):
    """Interface for reading sales data sources (CSV, DB, etc.)."""

    def read(self, file: Path) -> pd.DataFrame: ...


class Metric(Protocol):
    """Interface for computing a single metric."""

    def compute(self, df: pd.DataFrame) -> dict[str, object]: ...


# ------------------------------------------------------------------------------
# Core Classes
# ------------------------------------------------------------------------------


class CsvSalesReader:
    """Reads sales input data from a CSV file."""

    def read(self, file: Path) -> pd.DataFrame:
        logger.info("Reading data from %s", file)
        return pd.read_csv(file, parse_dates=["date"])  # pyright: ignore[reportUnknownMemberType]


class DateRangeFilter:
    """Filters sales data between a given start and end date."""

    def apply(self, df: pd.DataFrame, start: datetime | None, end: datetime | None) -> pd.DataFrame:
        logger.info("Applying date filter %s - %s", start or "N/A", end or "N/A")
        if start:
            df = df.loc[df["date"] >= pd.Timestamp(start)].copy()
        if end:
            df = df.loc[df["date"] <= pd.Timestamp(end)].copy()
        return df


# ------------------------------------------------------------------------------
# Metrics Implementations
# ------------------------------------------------------------------------------


class CustomerCountMetric:
    """Counts distinct customers in the dataset."""

    def compute(self, df: pd.DataFrame) -> dict[str, object]:
        return {"number_of_customers": df["name"].nunique()}


class AverageOrderValueMetric:
    """Computes the average positive order value (pre-tax)."""

    def compute(self, df: pd.DataFrame) -> dict[str, object]:
        sales = df.loc[df["price"] > 0, "price"]
        avg = sales.mean() if not sales.empty else 0.0
        return {"average_order_value (pre-tax)": round(avg, 2)}


class ReturnPercentageMetric:
    """Calculates what percentage of sales were returns."""

    def compute(self, df: pd.DataFrame) -> dict[str, object]:
        returns = df[df["price"] < 0]
        pct = (len(returns) / len(df)) * 100 if len(df) > 0 else 0
        return {"percentage_of_returns": round(pct, 2)}


class TotalSalesMetric:
    """Computes the total value of all transactions (pre-tax)."""

    def compute(self, df: pd.DataFrame) -> dict[str, object]:
        return {"total_sales_in_period (pre-tax)": round(df["price"].sum(), 2)}


# ------------------------------------------------------------------------------
# Generators and Writers
# ------------------------------------------------------------------------------


class SalesReportGenerator:
    """Coordinates the report creation process."""

    def __init__(self, reader: SalesReader, filterer: DateRangeFilter, metrics: list[Metric]):
        self.reader = reader
        self.filterer = filterer
        self.metrics = metrics

    def generate(self, config: ReportConfig) -> dict[str, object]:
        """Executes the complete reporting process: read → filter → compute."""

        df = self.reader.read(config.input_file)
        df = self.filterer.apply(df, config.start_date, config.end_date)

        logger.info("Computing metrics...")
        result: dict[str, object] = {}
        for metric in self.metrics:
            metric_data = metric.compute(df)
            result = result | metric_data

        result["report_start"] = (
            config.start_date.strftime("%Y-%m-%d") if config.start_date else "N/A"
        )
        result["report_end"] = config.end_date.strftime("%Y-%m-%d") if config.end_date else "N/A"
        return result


class JSONReportWriter:
    """Writes the report dictionary to a JSON file."""

    def write(self, report: dict[str, object], output_file: Path) -> None:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        logger.info("Report written to %s", output_file)


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------


def main() -> None:
    """Assembles and executes the OOP-style reporting workflow."""

    config = ReportConfig(
        input_file=INPUT_FILE,
        output_file=OUTPUT_FILE,
        start_date=REPORT_START,
        end_date=REPORT_END,
    )

    reader = CsvSalesReader()
    filterer = DateRangeFilter()
    metrics: list[Metric] = [
        CustomerCountMetric(),
        AverageOrderValueMetric(),
        ReturnPercentageMetric(),
        TotalSalesMetric(),
    ]

    generator = SalesReportGenerator(reader, filterer, metrics)
    writer = JSONReportWriter()

    try:
        report = generator.generate(config)
        writer.write(report, config.output_file)
    except Exception as e:
        logger.exception("Failed to generate report: %s", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
