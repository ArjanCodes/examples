import json
from typing import Protocol, Any

type Data = list[dict[str, Any]]


# === Interfaces ===
class DataLoader(Protocol):
    def load(self) -> Data: ...


class Transformer(Protocol):
    def transform(self, data: Data) -> Data: ...


class Exporter(Protocol):
    def export(self, data: Data) -> None: ...


# === Concrete Implementations ===
class InMemoryLoader:
    def load(self) -> Data:
        return [
            {"name": "Arjan", "age": 37},
            {"name": "Jane", "age": None},
            {"name": "Bob", "age": 45},
        ]


class CleanMissingFields:
    def transform(self, data: Data) -> Data:
        return [row for row in data if row["age"] is not None]


class JSONExporter:
    def __init__(self, filename: str):
        self.filename = filename

    def export(self, data: Data) -> None:
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)


# === Pipeline ===
class DataPipeline:
    def __init__(self, loader: DataLoader, transformer: Transformer, exporter: Exporter):
        self.loader = loader
        self.transformer = transformer
        self.exporter = exporter

    def run(self) -> None:
        data = self.loader.load()
        clean = self.transformer.transform(data)
        self.exporter.export(clean)


# === Main function: inject dependencies manually ===
def main() -> None:
    loader = InMemoryLoader()
    transformer = CleanMissingFields()
    exporter = JSONExporter("output.json")

    pipeline = DataPipeline(loader, transformer, exporter)
    pipeline.run()

    print("Pipeline completed. Output written to output.json")


if __name__ == "__main__":
    main()