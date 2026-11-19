"""
===============================================================================
Sales Report - Reactive (Stream-Based) Implementation
===============================================================================
Implements a reactive data pipeline using RxPY (Reactive Extensions for Python).

In a reactive system:
    * Data flows through Observables — streams that emit values.
    * Transformation steps are implemented as operators (map/filter/aggregate).
    * The pipeline is executed by subscribing to the observable chain.

Stages (mirroring previous paradigms):
    1. fetch_data     - Load data from CSV into stream
    2. process_data   - Filter by date range
    3. build_report   - Compute aggregate metrics
    4. write_report   - Persist computed summary to JSON
===============================================================================
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from rx import just
from rx import operators as ops

# ------------------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [reactive] %(message)s",
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
OUTPUT_FILE = OUTPUT_DIR / "sales_report_reactive.json"
REPORT_START = datetime(2024, 1, 1)
REPORT_END = datetime(2024, 12, 31)

# ------------------------------------------------------------------------------
# Reactive Pipeline Steps
# ------------------------------------------------------------------------------


def fetch_data(file: Path) -> pd.DataFrame:
    """Reads data from CSV into a pandas DataFrame."""

    logger.info("Reading data from %s", file)
    df = pd.read_csv(file, parse_dates=["date"])  # pyright: ignore[reportUnknownMemberType]
    logger.info("Data loaded successfully: %d rows", len(df))
    return df


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filters DataFrame by start and end date."""

    logger.info(
        "Filtering dataset from %s to %s",
        REPORT_START.strftime("%Y-%m-%d"),
        REPORT_END.strftime("%Y-%m-%d"),
    )
    filtered = df.loc[(df["date"] >= REPORT_START) & (df["date"] <= REPORT_END)].copy()
    logger.info("Filtered dataset contains %d rows", len(filtered))
    return filtered


def build_report(df: pd.DataFrame) -> dict[str, Any]:
    """Computes high-level report metrics from the dataset."""
    logger.info("Computing metrics...")

    number_of_customers = int(df["name"].nunique())
    positive_sales = df.loc[df["price"] > 0, "price"]
    avg_order_value = positive_sales.mean() if not positive_sales.empty else 0.0
    returns = df.loc[df["price"] < 0]
    pct_returns = (len(returns) / len(df)) * 100 if len(df) else 0.0
    total_sales = df["price"].sum()

    report = {
        "number_of_customers": number_of_customers,
        "average_order_value (pre-tax)": round(avg_order_value, 2),
        "percentage_of_returns": round(pct_returns, 2),
        "total_sales_in_period (pre-tax)": round(float(total_sales), 2),
        "report_start": REPORT_START.strftime("%Y-%m-%d"),
        "report_end": REPORT_END.strftime("%Y-%m-%d"),
    }

    logger.info("Metric computation complete.")
    return report


def write_report(report: dict[str, Any]) -> None:
    """Writes final report to disk."""
    OUTPUT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Report written to %s", OUTPUT_FILE)


# ------------------------------------------------------------------------------
# Reactive Pipeline Composition
# ------------------------------------------------------------------------------


def reactive_report_pipeline():
    """Builds and executes the reactive data pipeline using RxPY."""

    return (
        just(INPUT_FILE)
        .pipe(
            ops.map(fetch_data),  # pyright: ignore[reportUnknownMemberType]
            ops.map(process_data),  # pyright: ignore[reportUnknownMemberType]
            ops.map(build_report),  # pyright: ignore[reportUnknownMemberType]
        )
        .subscribe(
            on_next=write_report,
            on_error=lambda e: logger.exception("Pipeline failed: %s", e),  # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]
            on_completed=lambda: logger.info("Pipeline completed successfully."),
        )
    )


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting reactive sales report pipeline...")
    try:
        reactive_report_pipeline()
    except Exception as e:
        logger.exception("Unhandled error: %s", e)
        raise SystemExit(1) from e
