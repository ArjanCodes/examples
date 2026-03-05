import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class Summary:
    count: int
    revenue_sum: float


# ---------- Clean-looking abstraction ----------


class ReportService(Protocol):
    def run(self, source: str, target: str) -> None: ...


# ---------- Implementation with orthogonal complexity ----------


class DefaultReportService:
    def __init__(
        self,
        *,
        delimiter: str,
        encoding: str,
        country: str,
        min_revenue: float,
        allow_negative: bool,
    ) -> None:
        self._delimiter = delimiter
        self._encoding = encoding
        self._country = country
        self._min_revenue = min_revenue
        self._allow_negative = allow_negative

    def run(self, source: str, target: str) -> None:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(path)

        # --- Load ---
        with path.open("r", newline="", encoding=self._encoding) as f:
            reader = csv.DictReader(f, delimiter=self._delimiter)
            rows = [dict(r) for r in reader]

        # --- Validate + Filter + Aggregate ---
        count = 0
        revenue_sum = 0.0

        for r in rows:
            country = r.get("country")
            revenue_raw = r.get("revenue")

            if not country or not revenue_raw:
                continue

            revenue = float(revenue_raw)

            if revenue < 0 and not self._allow_negative:
                continue

            if country != self._country:
                continue

            if revenue < self._min_revenue:
                continue

            count += 1
            revenue_sum += revenue

        summary = Summary(count=count, revenue_sum=revenue_sum)

        # --- Export (two output options) ---
        text = (
            f"Country={self._country}, "
            f"Count={summary.count}, "
            f"Revenue={summary.revenue_sum:.2f}"
        )

        if target == "stdout":
            print(text)
        else:
            output_path = Path(target)
            output_path.write_text(text + "\n", encoding=self._encoding)
            print(f"Wrote report to {output_path.resolve()}")


# ---------- "DI container" wiring ----------


class Container:
    def __init__(self) -> None:
        self._settings = {
            "delimiter": ",",
            "encoding": "utf-8",
            "country": "NL",
            "min_revenue": 10.0,
            "allow_negative": False,
        }

    def report_service(self) -> ReportService:
        return DefaultReportService(**self._settings)


# ---------- Clean call site ----------


def main() -> None:
    service = Container().report_service()

    # Option 1: stdout
    service.run("sales.csv", "stdout")

    # Option 2: file output
    service.run("sales.csv", "report.txt")


if __name__ == "__main__":
    main()
