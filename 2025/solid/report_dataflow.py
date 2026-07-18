"""
===============================================================================
Sales Report - Dataflow (DAG) Implementation
===============================================================================
Implements the report workflow as a declarative Dataflow Graph (Directed
Acyclic Graph). Each node represents a data transformation or side effect.

Execution is topologically ordered based on declared dependencies —
the flow of data, not the order of code, determines execution.

Highlights:
    * Explicit dependency graph (no implicit control flow)
    * Reusable dataflow engine
    * Great for illustrating data-oriented design patterns
===============================================================================
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import pandas as pd

# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [dataflow] %(message)s",
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
OUTPUT_FILE = OUTPUT_DIR / "sales_report_dataflow.json"
REPORT_START = datetime(2024, 1, 1)
REPORT_END = datetime(2024, 12, 31)

# ------------------------------------------------------------------------------
# Dataflow Engine
# ------------------------------------------------------------------------------


class Node:
    """Represents a single transformation node in the DAG."""

    def __init__(
        self,
        name: str,
        func: Callable[..., Any],
        dependencies: list[str] | None = None,
    ):
        self.name = name
        self.func = func
        self.dependencies = dependencies or []
        self.result: Any = None


class DAG:
    """Lightweight dataflow DAG executor."""

    def __init__(self):
        self.nodes: dict[str, Node] = {}

    def add(self, name: str, func: Callable[..., Any], deps: list[str] | None = None):
        if name in self.nodes:
            raise ValueError(f"Node '{name}' already exists.")
        self.nodes[name] = Node(name, func, deps)

    def _resolve_order(self) -> list[Node]:
        """Topologically sort nodes based on declared dependencies."""
        visited: set[str] = set()
        order: list[Node] = []

        def visit(n: str):
            if n in visited:
                return
            node = self.nodes.get(n)
            if not node:
                raise ValueError(f"Node '{n}' not found in DAG.")
            for dep in node.dependencies:
                visit(dep)
            visited.add(n)
            order.append(node)

        for name in self.nodes:
            visit(name)

        return order

    def run(self):
        """Execute nodes in topological order, passing results between them."""
        logger.info("Executing dataflow pipeline...")
        order = self._resolve_order()
        results: dict[str, Any] = {}

        for node in order:
            kwargs = {dep: results[dep] for dep in node.dependencies}
            logger.info("→ Running %s ...", node.name)
            node.result = node.func(**kwargs)
            results[node.name] = node.result

        logger.info("Dataflow pipeline completed successfully.")
        return results


# ------------------------------------------------------------------------------
# Step Functions (pure transformations)
# ------------------------------------------------------------------------------


def read_data() -> pd.DataFrame:
    logger.info("Reading CSV from %s", INPUT_FILE)
    df = pd.read_csv(INPUT_FILE, parse_dates=["date"])
    logger.info("Loaded %d records.", len(df))
    return df


def filter_data(read_data: pd.DataFrame) -> pd.DataFrame:
    logger.info("Filtering dates between %s and %s", REPORT_START, REPORT_END)
    df = read_data[
        (read_data["date"] >= pd.Timestamp(REPORT_START))
        & (read_data["date"] <= pd.Timestamp(REPORT_END))
    ].copy()
    logger.info("Filtered %d records.", len(df))
    return df


def compute_metrics(filter_data: pd.DataFrame) -> dict[str, Any]:
    logger.info("Computing metrics declaratively...")

    positive_sales = filter_data.loc[filter_data["price"] > 0, "price"]
    returns = filter_data.loc[filter_data["price"] < 0, "price"]

    num_customers = filter_data["name"].nunique()
    avg_order_value = positive_sales.mean() if not positive_sales.empty else 0.0
    pct_returns = (len(returns) / len(filter_data)) * 100 if len(filter_data) else 0.0
    total_sales = filter_data["price"].sum()

    report = {
        "number_of_customers": int(num_customers),
        "average_order_value (pre-tax)": round(avg_order_value, 2),
        "percentage_of_returns": round(pct_returns, 2),
        "total_sales_in_period (pre-tax)": round(total_sales, 2),
        "report_start": REPORT_START.strftime("%Y-%m-%d"),
        "report_end": REPORT_END.strftime("%Y-%m-%d"),
    }
    return report


def write_report(compute_metrics: dict[str, Any]) -> None:
    OUTPUT_FILE.write_text(json.dumps(compute_metrics, indent=2), encoding="utf-8")
    logger.info("Report written to %s", OUTPUT_FILE)


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------


def main() -> None:
    """Constructs and runs the dataflow DAG."""
    logger.info("Starting Dataflow (DAG) Sales Report...")

    dag = DAG()
    dag.add("read_data", read_data)
    dag.add("filter_data", filter_data, deps=["read_data"])
    dag.add("compute_metrics", compute_metrics, deps=["filter_data"])
    dag.add("write_report", write_report, deps=["compute_metrics"])

    try:
        dag.run()
    except Exception as e:
        logger.exception("Dataflow pipeline failed: %s", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()