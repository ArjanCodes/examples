import json
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

import pandas as pd


@dataclass
class ReportConfig:
    input_file: str
    output_file: str
    start_date: datetime | None = None
    end_date: datetime | None = None


class SalesReader(Protocol):
    def read(self, file: str) -> pd.DataFrame: ...


class CsvSalesReader:
    def read(self, file: str) -> pd.DataFrame:
        return pd.read_csv(file, parse_dates=["date"])


class DateRangeFilter:
    def apply(
        self, df: pd.DataFrame, start: datetime | None, end: datetime | None
    ) -> pd.DataFrame:
        if start:
            df = df[df["date"] >= pd.Timestamp(start)]
        if end:
            df = df[df["date"] <= pd.Timestamp(end)]
        return df


class Metric(Protocol):
    def compute(self, df: pd.DataFrame) -> dict[str, object]: ...


class CustomerCountMetric:
    def compute(self, df: pd.DataFrame) -> dict[str, object]:
        return {"number_of_customers": df["name"].nunique()}


class AverageOrderValueMetric:
    def compute(self, df: pd.DataFrame) -> dict[str, object]:
        sales = df[df["price"] > 0]["price"]
        avg = sales.mean() if not sales.empty else 0.0
        return {"average_order_value (pre-tax)": round(avg, 2)}


class ReturnPercentageMetric:
    def compute(self, df: pd.DataFrame) -> dict[str, object]:
        returns = df[df["price"] < 0]
        pct = (len(returns) / len(df)) * 100 if len(df) > 0 else 0
        return {"percentage_of_returns": round(pct, 2)}


class TotalSalesMetric:
    def compute(self, df: pd.DataFrame) -> dict[str, object]:
        return {"total_sales_in_period (pre-tax)": round(df["price"].sum(), 2)}


class SalesReportGenerator:
    def __init__(
        self, reader: SalesReader, filterer: DateRangeFilter, metrics: list[Metric]
    ):
        self.reader = reader
        self.filterer = filterer
        self.metrics = metrics

    def generate(self, config: ReportConfig) -> dict[str, object]:
        df = self.reader.read(config.input_file)
        df = self.filterer.apply(df, config.start_date, config.end_date)

        result = {}
        for metric in self.metrics:
            result.update(metric.compute(df))

        result["report_start"] = (
            config.start_date.strftime("%Y-%m-%d") if config.start_date else "N/A"
        )
        result["report_end"] = (
            config.end_date.strftime("%Y-%m-%d") if config.end_date else "N/A"
        )
        return result


class JSONReportWriter:
    def write(self, report: dict[str, object], output_file: str) -> None:
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)


def main() -> None:
    config = ReportConfig(
        input_file="sales_data.csv",
        output_file="sales_report.json",
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),
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
    report = generator.generate(config)

    writer = JSONReportWriter()
    writer.write(report, config.output_file)


if __name__ == "__main__":
    main()
