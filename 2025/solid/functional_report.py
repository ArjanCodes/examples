import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable

import pandas as pd

type MetricFn = Callable[[pd.DataFrame], dict[str, Any]]


@dataclass
class ReportConfig:
    input_file: str
    start_date: datetime | None = None
    end_date: datetime | None = None
    metrics: list[MetricFn] = field(default_factory=list)


def read_sales(file: str) -> pd.DataFrame:
    return pd.read_csv(file, parse_dates=["date"])


def filter_sales(
    df: pd.DataFrame, start: datetime | None, end: datetime | None
) -> pd.DataFrame:
    if start:
        df = df[df["date"] >= pd.Timestamp(start)]
    if end:
        df = df[df["date"] <= pd.Timestamp(end)]
    return df


def customer_count_metric(df: pd.DataFrame) -> dict[str, Any]:
    return {"number_of_customers": df["name"].nunique()}


def average_order_value_metric(df: pd.DataFrame) -> dict[str, Any]:
    sales = df[df["price"] > 0]["price"]
    avg = sales.mean() if not sales.empty else 0.0
    return {"average_order_value (pre-tax)": round(avg, 2)}


def return_percentage_metric(df: pd.DataFrame) -> dict[str, Any]:
    returns = df[df["price"] < 0]
    pct = (len(returns) / len(df)) * 100 if len(df) > 0 else 0
    return {"percentage_of_returns": round(pct, 2)}


def total_sales_metric(df: pd.DataFrame) -> dict[str, Any]:
    return {"total_sales_in_period (pre-tax)": round(df["price"].sum(), 2)}


def generate_report_data(df: pd.DataFrame, config: ReportConfig) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for metric in config.metrics:
        result.update(metric(df))
    result["report_start"] = (
        config.start_date.strftime("%Y-%m-%d") if config.start_date else "N/A"
    )
    result["report_end"] = (
        config.end_date.strftime("%Y-%m-%d") if config.end_date else "N/A"
    )
    return result


def write_report(data: dict[str, Any], filename: str):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def main() -> None:
    config = ReportConfig(
        input_file="sales_data.csv",
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),
        metrics=[
            customer_count_metric,
            average_order_value_metric,
            return_percentage_metric,
            total_sales_metric,
        ],
    )

    df = read_sales(config.input_file)
    df = filter_sales(df, config.start_date, config.end_date)
    report_data = generate_report_data(df, config)
    write_report(report_data, "sales_report.json")


if __name__ == "__main__":
    main()
