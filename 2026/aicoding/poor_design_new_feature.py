import csv
import io
import json
from dataclasses import asdict
from typing import Literal

from openpyxl import Workbook
from poor_design_before import SalesRecord
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ReportFormat = Literal["csv", "json", "pdf", "xlsx"]


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

    elif format == "xlsx":
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

    else:
        raise ValueError(f"Unsupported format: {format}")
