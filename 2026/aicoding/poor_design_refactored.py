import csv
import io
import json
from collections.abc import Callable
from dataclasses import asdict, dataclass

from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


@dataclass(frozen=True)
class SalesRecord:
    product: str
    quantity: int
    revenue: float


# Each generator accepts sales records and returns file content.
type ReportGenerator = Callable[[list[SalesRecord]], bytes]


def generate_csv(records: list[SalesRecord]) -> bytes:
    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=["product", "quantity", "revenue"],
    )
    writer.writeheader()
    writer.writerows(asdict(record) for record in records)

    return output.getvalue().encode("utf-8")


def generate_json(records: list[SalesRecord]) -> bytes:
    data = [asdict(record) for record in records]
    return json.dumps(data, indent=2).encode("utf-8")


def generate_pdf(records: list[SalesRecord]) -> bytes:
    output = io.BytesIO()
    pdf = canvas.Canvas(output, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, "Sales Report")

    pdf.setFont("Helvetica", 11)
    y = 760

    for record in records:
        pdf.drawString(
            50,
            y,
            f"{record.product}: {record.quantity} sold, EUR {record.revenue:.2f}",
        )
        y -= 20

    pdf.save()
    return output.getvalue()


def generate_excel(records: list[SalesRecord]) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    assert sheet is not None

    sheet.title = "Sales"
    sheet.append(["Product", "Quantity", "Revenue"])

    for record in records:
        sheet.append(
            [
                record.product,
                record.quantity,
                record.revenue,
            ]
        )

    output = io.BytesIO()
    workbook.save(output)

    return output.getvalue()


# Map each format to its generator function.
GENERATORS: dict[str, ReportGenerator] = {
    "csv": generate_csv,
    "json": generate_json,
    "pdf": generate_pdf,
    "xlsx": generate_excel,
}


def generate_report(
    records: list[SalesRecord],
    format: str,
) -> bytes:
    try:
        generator = GENERATORS[format]
    except KeyError:
        raise ValueError(f"Unsupported report format: {format}") from None

    return generator(records)


def main() -> None:
    records = [
        SalesRecord("Laptop", 12, 14400.0),
        SalesRecord("Monitor", 25, 6250.0),
        SalesRecord("Keyboard", 40, 3200.0),
    ]

    for format in GENERATORS:
        content = generate_report(records, format)

        with open(f"report.{format}", "wb") as file:
            file.write(content)

        print(f"Generated report.{format}")


if __name__ == "__main__":
    main()
