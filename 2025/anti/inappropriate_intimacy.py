import json
from dataclasses import dataclass
from typing import Callable


@dataclass
class Report:
    title: str
    content: str

    def to_csv(self) -> str:
        return f"{self.title}, {self.content}\n"

    def to_json(self) -> str:
        return json.dumps(
            {
                "title": self.title,
                "content": self.content,
            },
            indent=4,
        )


type ExportFn = Callable[[str, Report], None]


def export_to_csv(filename: str, report: Report) -> None:
    print("Exporting to CSV...")
    with open(filename, "w") as f:
        f.write(report.to_csv())
    print("Done.")


def export_to_json(filename: str, report: Report) -> None:
    print("Exporting to JSON...")
    with open(filename, "w") as f:
        json.dump(report.to_json(), f)
    print("Done.")


EXPORTERS = {
    "csv": export_to_csv,
    "json": export_to_json,
}


def get_exporter(format: str) -> ExportFn:
    """Factory function to get the appropriate exporter function based on format string."""
    if format in EXPORTERS:
        return EXPORTERS[format]
    else:
        raise ValueError(f"Unsupported export format: {format}")


def main() -> None:
    report = Report(
        title="Quarterly Earnings",
        content="Here are the earnings for the last quarter...",
    )

    export_fn = get_exporter("json")
    export_fn("report.json", report)


if __name__ == "__main__":
    main()
