from dataclasses import dataclass
from typing import Optional

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen.canvas import Canvas

from writer.invoice import Invoice


class PdfExporter:
    def __init__(self, filename: str) -> None:
        self.left_margin = 72
        self.top_margin = 72
        self.canvas = Canvas(filename, pagesize=LETTER)
        self.line_height = 16

    def export(self, invoice: Invoice):

        # translate to the top
        x, y = LETTER
        self.canvas.translate(self.left_margin, y - self.top_margin)
        self.write_line("Invoice for:")
        self.write_line(invoice.customer.name)
        self.write_line(invoice.customer.address)
        self.write_line(invoice.customer.phone)
        self.write_line(invoice.customer.email)
        self.write_line()

        self.canvas.save()

    def write(self, text: str):
        self.canvas.drawString(0, 0, text)

    def write_line(self, text: str = ""):
        self.write(text)
        self.canvas.translate(0, -self.line_height)
