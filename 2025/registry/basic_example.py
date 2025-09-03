from functools import wraps
from typing import Any, Callable

type Data = dict[str, Any]
type ExportFn = Callable[[Data], None]

# The registry: maps format name to export function
exporters: dict[str, ExportFn] = {}


def register_exporter(name: str):
    def decorator(func: ExportFn):
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        exporters[name] = wrapper
        return wrapper

    return decorator


@register_exporter("pdf")
def export_pdf(data: Data) -> None:
    print(f"Exporting data to PDF: {data}")


@register_exporter("csv")
def export_csv(data: Data) -> None:
    print(f"Exporting data to CSV: {data}")


@register_exporter("json")
def export_json(data: Data) -> None:
    import json

    print("Exporting data to JSON:")
    print(json.dumps(data, indent=2))


def export_data(data: Data, format: str) -> None:
    exporter = exporters.get(format)
    if exporter is None:
        raise ValueError(f"❌ No exporter found for format: {format}")
    exporter(data)


def main() -> None:
    sample_data: Data = {"name": "Alice", "age": 30}

    # Try exporting in different formats
    export_data(sample_data, "pdf")
    export_data(sample_data, "csv")
    export_data(sample_data, "json")

    # This would raise an error:
    export_data(sample_data, "xlsx")


if __name__ == "__main__":
    main()
