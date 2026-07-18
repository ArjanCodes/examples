"""
===============================================================================
Sales Report — Logic-Based Version
===============================================================================
Implements the same declarative logic reporting system, but without relying on
numeric constraint solvers.  Instead, we encode the idea of "positive" and
"negative" prices as pure logic facts.

All reasoning is relational and declarative; no imperative filtering is used.
===============================================================================
"""

import json
import logging
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, cast

import pandas as pd
from kanren import Relation, Var, var
from kanren import conde as _conde  # pyright: ignore[reportUnknownVariableType]
from kanren import facts as _facts  # pyright: ignore[reportUnknownVariableType]
from kanren import run as _run  # pyright: ignore[reportUnknownVariableType]

type Goal = Any
type LogicVar = Var | Any
type Sign = Literal["positive", "negative", "zero"]
type ProfitRecord = tuple[str, float]
type MetricValue = float | int | str
type ReportDict = dict[str, MetricValue]

CondeFunc = Callable[..., Goal]
RunFunc = Callable[..., Sequence[Any] | tuple[Any, ...]]

conde: CondeFunc = cast(CondeFunc, _conde)
facts: Callable[..., None] = cast(Callable[..., None], _facts)
run: RunFunc = cast(RunFunc, _run)

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [logic‑pure] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "sales_data.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "sales_report_logic.json"
REPORT_START = datetime(2024, 1, 1)
REPORT_END = datetime(2024, 12, 31)


# -----------------------------------------------------------------------------
# Data representation
# -----------------------------------------------------------------------------
@dataclass
class Sale:
    name: str
    item: str
    date: datetime
    price: float
    tax: float


# -----------------------------------------------------------------------------
# Load CSV data
# -----------------------------------------------------------------------------
def load_sales(file_path: Path) -> list[Sale]:
    df = pd.read_csv(file_path, parse_dates=["date"])  # pyright: ignore
    df = df.loc[(df["date"] >= REPORT_START) & (df["date"] <= REPORT_END)]
    logger.info("Loaded %d sales within reporting window.", len(df))
    return [
        Sale(row["name"], row["item"], row["date"], row["price"], row["tax"])
        for _, row in df.iterrows()
    ]


# -----------------------------------------------------------------------------
# Logic Relations
# -----------------------------------------------------------------------------


def declare_relations(sales: list[Sale]) -> tuple[Relation, Relation]:
    """
    Declare logic base facts for sales and price sign.

    sign_rel(price_sign, price)
        'price_sign' is one of {"positive", "negative", "zero"}.
    """
    sale_rel = Relation()
    sign_rel = Relation()

    # Declare base sale facts
    for s in sales:
        facts(sale_rel, (s.name, s.item, s.date, s.price, s.tax))

    # Build pure logic 'sign' facts — not procedural checks within the logic
    unique_prices: list[float] = sorted({float(s.price) for s in sales})
    for price_value in unique_prices:
        # Outside the logic system, we merely declare new *facts*,
        # analogous to telling Prolog that sign(positive, 10.0). is true.
        if price_value > 0:
            facts(sign_rel, (cast(Sign, "positive"), price_value))
        elif price_value < 0:
            facts(sign_rel, (cast(Sign, "negative"), price_value))
        else:
            facts(sign_rel, (cast(Sign, "zero"), price_value))

    logger.info("Declared %d sale facts and %d sign facts.", len(sales), len(unique_prices))
    return sale_rel, sign_rel


# -----------------------------------------------------------------------------
# Logic predicates (pure relations)
# -----------------------------------------------------------------------------
def sign_rule(sign_rel: Relation, sign: Sign, price: Any) -> Goal:
    """Link a price to its logical sign fact."""
    return cast(Goal, sign_rel(sign, price))


def profit_rule(sale_rel: Relation, sign_rel: Relation, name: Any, price: Any) -> Goal:
    """Logical predicate for profitable sales (positive price)."""
    return conde(
        [
            sale_rel(name, var(), var(), price, var()),
            sign_rule(sign_rel, cast(Sign, "positive"), price),
        ]
    )


def return_rule(sale_rel: Relation, sign_rel: Relation, name: Any, price: Any) -> Goal:
    """Logical predicate for returned sales (negative price)."""
    return conde(
        [
            sale_rel(name, var(), var(), price, var()),
            sign_rule(sign_rel, cast(Sign, "negative"), price),
        ]
    )


# -----------------------------------------------------------------------------
# Logic computations — querying the pure logic model
# -----------------------------------------------------------------------------
def compute_metrics(sale_rel: Relation, sign_rel: Relation) -> ReportDict:
    """Compute metrics via logical queries only."""

    name: LogicVar = cast(LogicVar, var())
    price: LogicVar = cast(LogicVar, var())

    profit_raw = cast(
        Sequence[tuple[Any, Any]],
        run(0, (name, price), profit_rule(sale_rel, sign_rel, name, price)),
    )
    return_raw = cast(
        Sequence[tuple[Any, Any]],
        run(0, (name, price), return_rule(sale_rel, sign_rel, name, price)),
    )

    def _filter_records(records: Sequence[tuple[Any, Any]]) -> list[ProfitRecord]:
        filtered: list[ProfitRecord] = []
        for raw_name, raw_price in records:
            if isinstance(raw_name, str) and isinstance(raw_price, (int, float)):
                filtered.append((raw_name, float(raw_price)))
        return filtered

    profit_records = _filter_records(profit_raw)
    return_records = _filter_records(return_raw)

    # Summarize results outside logic
    profit_customers = {name_value for (name_value, _) in profit_records}
    return_customers = {name_value for (name_value, _) in return_records}
    profit_prices = [price_value for (_, price_value) in profit_records]
    return_prices = [price_value for (_, price_value) in return_records]

    num_customers = len(profit_customers | return_customers)
    avg_order_value = sum(profit_prices) / len(profit_prices) if profit_prices else 0.0
    pct_returns = (
        len(return_prices) / (len(profit_prices) + len(return_prices)) * 100
        if (profit_prices or return_prices)
        else 0.0
    )
    total_sales = sum(profit_prices) + sum(return_prices)

    return {
        "number_of_customers": num_customers,
        "average_order_value (pre-tax)": round(avg_order_value, 2),
        "percentage_of_returns": round(pct_returns, 2),
        "total_sales_in_period (pre-tax)": round(total_sales, 2),
        "report_start": REPORT_START.strftime("%Y-%m-%d"),
        "report_end": REPORT_END.strftime("%Y-%m-%d"),
    }


# -----------------------------------------------------------------------------
# Writer
# -----------------------------------------------------------------------------
def write_report(report: ReportDict) -> None:
    OUTPUT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Logic report written to %s", OUTPUT_FILE)


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
def main() -> None:
    logger.info("Running logic sales report ...")
    try:
        sales = load_sales(DATA_PATH)
        if not sales:
            logger.warning("No sales data in reporting window.")
            return
        sale_rel, sign_rel = declare_relations(sales)
        report = compute_metrics(sale_rel, sign_rel)
        write_report(report)
        logger.info("Logic report generated successfully.")
    except Exception as exc:
        logger.exception("Logic computation failed: %s", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
