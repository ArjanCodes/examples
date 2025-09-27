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
    def __ini__(self, file: str):
        self.file = file

    def read(self) -> pd.DataFrame:
        return pd.read_csv(self.file, parse_dates=["date"])


class DateRangeFilter:
    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end

    def apply(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        if self.start:
            df = df[df["date"] >= pd.Timestamp(self.start)]
        if self.end:
            df = df[df["date"] <= pd.Timestamp(self.end)]
        return df


class Report(Protocol):
    def report(self, df: pd.DataFrame=None) -> dict[str, object]: ...


class CustomerCountReport:
    def report(self, df: pd.DataFrame) -> dict[str, object]:
        return {"number_of_customers": df["name"].nunique()}


class AverageOrderValueReport:
    def report(self, df: pd.DataFrame) -> dict[str, object]:
        sales = df[df["price"] > 0]["price"]
        avg = sales.mean() if not sales.empty else 0.0
        return {"average_order_value (pre-tax)": round(avg, 2)}


class ReturnPercentageReport:
    def report(self, df: pd.DataFrame) -> dict[str, object]:
        returns = df[df["price"] < 0]
        pct = (len(returns) / len(df)) * 100 if len(df) > 0 else 0
        return {"percentage_of_returns": round(pct, 2)}


class TotalSalesReport:
    def report(self, df: pd.DataFrame) -> dict[str, object]:
        return {"total_sales_in_period (pre-tax)": round(df["price"].sum(), 2)}


class DateRangeReport:
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date
        
    def report(self, df: pd.DataFrame) -> dict[str, object]:
        return {
            "report_start": self.start_date.strftime("%Y-%m-%d") if self.start_date else "N/A",
            "report_end": self.end_date.strftime("%Y-%m-%d") if self.end_date else "N/A"
        }


class SalesReportGenerator:
    def __init__(
        self, reader: SalesReader, filterer: DateRangeFilter, Reports: list[Report]
    ):
        self.reader = reader
        self.filterer = filterer
        self.Reports = Reports

    def generate(self) -> dict[str, object]:
        df = self.reader.read()
        df = self.filterer.apply(df)

        result = {}
        for Report in self.Reports:
            result.update(Report.report(df))

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

    reader = CsvSalesReader(file=config.input_file)
    filterer = DateRangeFilter(config.start_date, config.end_date)
    Reports: list[Report] = [
        CustomerCountReport(),
        AverageOrderValueReport(),
        ReturnPercentageReport(),
        TotalSalesReport(),
        DateRangeReport(config.start_date, config.end_date),
    ]

    generator = SalesReportGenerator(reader, filterer, Reports)
    report = generator.generate()

    writer = JSONReportWriter()
    writer.write(report, config.output_file)


if __name__ == "__main__":
    main()
