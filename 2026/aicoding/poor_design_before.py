import csv
import io
import json
from dataclasses import asdict, dataclass
from typing import Literal

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


@dataclass(frozen=True)
class SalesRecord:
    product: str
    quantity: int
    revenue: float


ReportFormat = Literal["csv", "json", "pdf"]


def generate_report(
    records: list[SalesRecord],
    format: ReportFormat,
) -> bytes:
    if format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=["product", "quantity", "revenue"],
        )
        writer.writeheader()
        writer.writerows(asdict(record) for record in records)
        return output.getvalue().encode("utf-8")

    elif format == "json":
        data = [asdict(record) for record in records]
        return json.dumps(data, indent=2).encode("utf-8")

    elif format == "pdf":
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

    else:
        raise ValueError(f"Unsupported format: {format}")


def main() -> None:
    records = [
        SalesRecord("Laptop", 12, 14400.0),
        SalesRecord("Monitor", 25, 6250.0),
        SalesRecord("Keyboard", 40, 3200.0),
    ]

    for format in ("csv", "json", "pdf"):
        content = generate_report(records, format)
        with open(f"report.{format}", "wb") as file:
            file.write(content)

        print(f"Generated report.{format}")


if __name__ == "__main__":
    main()
