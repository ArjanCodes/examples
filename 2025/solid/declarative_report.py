"""
===============================================================================
Sales Report - Declarative (Pipeline) Implementation
===============================================================================
A declarative, type-safe data pipeline using Pandera for runtime validation
and pure function composition.

Stages:
    1. fetch_data     - Extract + validate CSV data
    2. process_data   - Transform by filtering rows to time window
    3. build_report   - Compute key metrics declaratively
    4. write_report   - Serialize results to JSON
===============================================================================
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

import pandas as pd
import pandera.pandas as pa
from pandera.typing import DataFrame

# ------------------------------------------------------------------------------
# Logging configuration
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Schema definition
# ------------------------------------------------------------------------------


class SalesSchema(pa.DataFrameModel):
    """Defines the expected structure and types for the input sales data."""

    date: datetime = pa.Field(coerce=True)
    name: str
    address: str
    item: str
    price: float
    tax: float


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "sales_data.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_PATH = OUTPUT_DIR / "sales_report_declarative.json"
REPORT_START_DATE = datetime(2024, 1, 1)
REPORT_END_DATE = datetime(2024, 12, 31)


# ------------------------------------------------------------------------------
# Data Pipeline Steps
# ------------------------------------------------------------------------------


def fetch_data(_: None) -> DataFrame[SalesSchema]:
    """Step 1: Read and validate input CSV file."""

    logger.info("Reading input data from %s", DATA_PATH)
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])  # pyright: ignore[reportUnknownMemberType]
    validated = SalesSchema.validate(df)
    logger.info("Data loaded successfully: %d rows", len(validated))
    return validated


def process_data(df: DataFrame[SalesSchema]) -> DataFrame[SalesSchema]:
    """Step 2: Filter the dataset to report date range."""

    logger.info(
        "Filtering records between %s and %s",
        REPORT_START_DATE.strftime("%Y-%m-%d"),
        REPORT_END_DATE.strftime("%Y-%m-%d"),
    )
    filtered = df.loc[(df["date"] >= REPORT_START_DATE) & (df["date"] <= REPORT_END_DATE)].copy()
    logger.info("Filtered dataset contains %d records", len(filtered))
    return SalesSchema.validate(filtered)


def build_report(df: DataFrame[SalesSchema]) -> dict[str, Any]:
    """Step 3: Compute key report metrics."""

    logger.info("Computing report metrics...")

    number_of_customers = int(df["name"].nunique())
    positive_sales = df.loc[df["price"] > 0, "price"]
    average_order_value = float(positive_sales.mean()) if not positive_sales.empty else 0.0
    returns = df.loc[df["price"] < 0]
    percentage_of_returns = (len(returns) / len(df)) * 100 if len(df) > 0 else 0.0
    total_sales_pre_tax = float(df["price"].sum())

    report = {
        "number_of_customers": number_of_customers,
        "average_order_value (pre-tax)": round(average_order_value, 2),
        "percentage_of_returns": round(percentage_of_returns, 2),
        "total_sales_in_period (pre-tax)": round(total_sales_pre_tax, 2),
        "report_start": REPORT_START_DATE.strftime("%Y-%m-%d"),
        "report_end": REPORT_END_DATE.strftime("%Y-%m-%d"),
    }
    logger.info("Completed metric calculations.")
    return report


def write_report(report: dict[str, Any]) -> None:
    """Step 4: Write final JSON report to disk."""

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Report written to: {REPORT_PATH}")


# ------------------------------------------------------------------------------
# Declarative Pipeline Orchestrator
# ------------------------------------------------------------------------------


class PipelineStep(Protocol):
    """Formal protocol for pipeline-compatible callables."""

    def __call__(self, __data: Any) -> Any: ...


def pipeline(*steps: PipelineStep):
    """
    Declaratively compose a pipeline of sequential transformation steps.

    Each step takes the output of the previous one.
    The first receives `None` if it doesn't need input.
    """

    def composed(data: Any = None) -> Any:
        for step in steps:
            data = step(data)
        return data

    return composed


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting declarative report pipeline...")
    try:
        report_pipeline = pipeline(
            fetch_data,
            process_data,
            build_report,
            write_report,
        )
        report_pipeline(None)
        logger.info("Report generation completed successfully.")
    except Exception as e:
        logger.exception("Failed to generate report: %s", e)
        raise SystemExit(1) from e
