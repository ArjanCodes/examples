import csv
import json
from dataclasses import dataclass
from pathlib import Path

type Data = dict[str, str]
type JSON = dict[str, str | int | float]


@dataclass(frozen=True)
class ReportConfig:
    country: str = "NL"
    min_revenue: float = 10.0
    allow_negative: bool = False
    delimiter: str = ","
    encoding: str = "utf-8"


@dataclass(frozen=True)
class Summary:
    country: str
    count: int
    revenue_sum: float

    def to_text(self) -> str:
        return (
            f"Country={self.country}, "
            f"Count={self.count}, "
            f"Revenue={self.revenue_sum:.2f}"
        )

    def to_json(self) -> JSON:
        return {
            "country": self.country,
            "count": self.count,
            "revenue_sum": self.revenue_sum,
        }


def load_data(source: Path, config: ReportConfig) -> list[Data]:
    if not source.exists():
        raise FileNotFoundError(source)

    with source.open("r", newline="", encoding=config.encoding) as f:
        reader = csv.DictReader(f, delimiter=config.delimiter)
        return [dict(r) for r in reader]


def summarize(rows: list[Data], config: ReportConfig) -> Summary:

    def is_valid(r: Data) -> bool:
        if not r.get("country") or not r.get("revenue"):
            return False

        revenue = float(r["revenue"])

        if revenue < 0 and not config.allow_negative:
            return False

        if r["country"] != config.country:
            return False

        if revenue < config.min_revenue:
            return False

        return True

    valid_rows = [r for r in rows if is_valid(r)]

    return Summary(
        country=config.country,
        count=len(valid_rows),
        revenue_sum=sum(float(r["revenue"]) for r in valid_rows),
    )


def export_stdout(summary: Summary) -> None:
    print(summary.to_text())


def export_file(summary: Summary, path: Path) -> None:
    path.write_text(summary.to_text() + "\n")
    print(f"Wrote report to {path.resolve()}")


def export_json(summary: Summary, path: Path) -> None:
    data = summary.to_json()
    path.write_text(json.dumps(data, indent=2))
    print(f"Wrote report to {path.resolve()}")


def main() -> None:
    config = ReportConfig(country="NL", min_revenue=10.0)
    rows = load_data(Path("sales.csv"), config)
    summary = summarize(rows, config)

    # Option 1: print to console
    export_stdout(summary)

    # Option 2: write to file
    export_file(summary, Path("report.txt"))

    # Option 3: write to JSON file
    export_json(summary, Path("report.json"))


if __name__ == "__main__":
    main()
