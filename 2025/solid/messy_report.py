import json
from datetime import datetime

import pandas as pd


class MessySalesReport:
    def generate(
        self,
        input_file: str,
        output_file: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> None:
        df = pd.read_csv(input_file, parse_dates=["date"])

        if start_date:
            df = df[df["date"] >= pd.Timestamp(start_date)]
        if end_date:
            df = df[df["date"] <= pd.Timestamp(end_date)]

        num_customers = df["name"].nunique()
        avg_order = (
            df[df["price"] > 0]["price"].mean() if not df[df["price"] > 0].empty else 0
        )
        returns = df[df["price"] < 0]
        return_pct = (len(returns) / len(df)) * 100 if len(df) > 0 else 0
        total_sales = df["price"].sum()

        report = {
            "report_start": start_date.strftime("%Y-%m-%d") if start_date else "N/A",
            "report_end": end_date.strftime("%Y-%m-%d") if end_date else "N/A",
            "number_of_customers": num_customers,
            "average_order_value (pre-tax)": round(avg_order, 2),
            "percentage_of_returns": round(return_pct, 2),
            "total_sales_in_period (pre-tax)": round(total_sales, 2),
        }

        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)


def main() -> None:
    report = MessySalesReport()
    report.generate(
        input_file="sales_data.csv",
        output_file="sales_report.json",
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),
    )


if __name__ == "__main__":
    main()
