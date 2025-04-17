import json
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Report:
    title: str
    content: str


class Exporter(ABC):
    """Abstract base class for data exporters."""

    @abstractmethod
    def export(self, filename: str, report: Report) -> None:
        pass


class CSVExporter(Exporter):
    """Exporter for CSV format."""

    def export(self, filename: str, report: Report) -> None:
        csv_data = f"{report.title}, {report.content}\n"
        print("Exporting to CSV...")
        with open(filename, "w") as f:
            f.write(csv_data)
        print("Done.")


class JSONExporter(Exporter):
    """Exporter for JSON format."""

    def export(self, filename: str, report: Report) -> None:
        print("Exporting to JSON...")
        json_data = {
            "title": report.title,
            "content": report.content,
        }
        with open(filename, "w") as f:
            json.dump(json_data, f)
        print("Done.")


class ExporterFactory:
    """Factory for creating exporters based on format string."""

    @staticmethod
    def get_exporter(format: str) -> Exporter:
        if format == "csv":
            return CSVExporter()
        elif format == "json":
            return JSONExporter()
        else:
            raise ValueError(f"Unsupported export format: {format}")


def main() -> None:
    report = Report(
        title="Quarterly Earnings",
        content="Here are the earnings for the last quarter...",
    )

    exporter = ExporterFactory.get_exporter("json")
    exporter.export("report.json", report)


if __name__ == "__main__":
    main()
