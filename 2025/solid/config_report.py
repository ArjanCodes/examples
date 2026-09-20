"""
===============================================================================
Sales Report - Config-Driven (Declarative) Implementation
===============================================================================
Loads pipeline configuration from an external YAML/JSON file and runs the
same metric logic dynamically, controlled entirely by configuration content.

Highlights:
    * Decouples logic from configuration
    * Allows multiple report variants without code modification
===============================================================================
"""

import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

# ------------------------------------------------------------------------------
# Logging Setup
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [config] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "report_config.yaml"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------------------------
# Metric Functions
# ------------------------------------------------------------------------------


def customer_count(df: pd.DataFrame) -> dict[str, Any]:
    """Counts distinct customers."""

    return {"number_of_customers": df["name"].nunique()}


def average_order_value(df: pd.DataFrame) -> dict[str, Any]:
    """Calculates average order value."""

    sales = df[df["price"] > 0]["price"]
    avg = sales.mean() if not sales.empty else 0.0
    return {"average_order_value (pre-tax)": round(avg, 2)}


def return_percentage(df: pd.DataFrame) -> dict[str, Any]:
    """Calculates percentage of returns."""

    returns = df[df["price"] < 0]
    pct = (len(returns) / len(df)) * 100 if len(df) else 0.0
    return {"percentage_of_returns": round(pct, 2)}


def total_sales(df: pd.DataFrame) -> dict[str, Any]:
    """Calculates total sales."""

    return {"total_sales_in_period (pre-tax)": round(df["price"].sum(), 2)}


METRIC_REGISTRY: dict[str, Callable[[pd.DataFrame], dict[str, Any]]] = {
    "customer_count": customer_count,
    "average_order_value": average_order_value,
    "return_percentage": return_percentage,
    "total_sales": total_sales,
}

# ------------------------------------------------------------------------------
# Config Schema
# ------------------------------------------------------------------------------


@dataclass
class ReportConfig:
    dataset: Path
    start_date: datetime | None
    end_date: datetime | None
    metrics: list[str]
    output_file: Path


# ------------------------------------------------------------------------------
# Core Functions
# ------------------------------------------------------------------------------


def load_config(file: Path) -> ReportConfig:
    """Loads YAML config and converts to ReportConfig dataclass."""
    with open(file, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return ReportConfig(
        dataset=BASE_DIR / data["dataset"],
        start_date=datetime.fromisoformat(data["start_date"]),
        end_date=datetime.fromisoformat(data["end_date"]),
        metrics=data["metrics"],
        output_file=BASE_DIR / data["output"],
    )


def run_pipeline(config: ReportConfig) -> dict[str, Any]:
    """Executes report pipeline as declared in YAML config."""
    logger.info("Loading dataset %s", config.dataset)
    df = pd.read_csv(config.dataset, parse_dates=["date"])  # pyright: ignore[reportUnknownMemberType]

    # Apply filters
    if config.start_date:
        df = df[df["date"] >= pd.Timestamp(config.start_date)]
    if config.end_date:
        df = df[df["date"] <= pd.Timestamp(config.end_date)]
    logger.info("Records after filtering: %d", len(df))

    # Compute declared metrics dynamically
    results: dict[str, Any] = {}
    for metric_key in config.metrics:
        metric_fn = METRIC_REGISTRY.get(metric_key)
        if metric_fn:
            results.update(metric_fn(df))
        else:
            logger.warning("Unknown metric '%s' skipped.", metric_key)

    results["report_start"] = config.start_date.strftime("%Y-%m-%d") if config.start_date else "N/A"
    results["report_end"] = config.end_date.strftime("%Y-%m-%d") if config.end_date else "N/A"
    return results


def write_report(report: dict[str, Any], output: Path) -> None:
    """Writes report to JSON file."""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Config-based report written to %s", output)


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------


def main() -> None:
    config = load_config(CONFIG_FILE)
    logger.info("Running config-driven report using %s", CONFIG_FILE)
    try:
        result = run_pipeline(config)
        write_report(result, config.output_file)
        logger.info("Report generated successfully.")
    except Exception as e:
        logger.exception("Failed to generate report: %s", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
