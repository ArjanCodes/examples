import json
from dataclasses import dataclass
from typing import Callable, Protocol


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


@dataclass
class Budget:
    title: str
    amount: float

    def to_csv(self) -> str:
        return f"{self.title}, {self.amount}\n"

    def to_json(self) -> str:
        return json.dumps(
            {
                "title": self.title,
                "amount": self.amount,
            },
            indent=4,
        )


type ExportFn = Callable[[str, Exportable], None]


class Exportable(Protocol):
    def to_csv(self) -> str: ...

    def to_json(self) -> str: ...


def export_to_csv(filename: str, data: Exportable) -> None:
    print("Exporting to CSV...")
    with open(filename, "w") as f:
        f.write(data.to_csv())
    print("Done.")


def export_to_json(filename: str, data: Exportable) -> None:
    print("Exporting to JSON...")
    with open(filename, "w") as f:
        json.dump(data.to_json(), f)
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

    budget = Budget(
        title="Annual Budget",
        amount=1000000.00,
    )

    export_fn = get_exporter("json")
    export_fn("budget.json", budget)


if __name__ == "__main__":
    main()
