from datetime import datetime

from writer.exporter import Exporter
from writer.invoice import Customer, Invoice, LineItem
from writer.pdf_exporter import PdfExporter
from writer.text_exporter import TextExporter


def export_invoice(invoice: Invoice, exporter: Exporter) -> None:
    exporter.export(invoice)


def main():
    customer = Customer(
        name="John Smith",
        address="123 Fake Street",
        phone="0123456789",
        email="john@smith.com",
    )
    invoice = Invoice(reference="2022-1345", date=datetime.now(), customer=customer)
    invoice.add_item(LineItem("Item 1", 2, 50_00))
    invoice.add_item(LineItem("Item 2", 1, 100_00))

    export_invoice(invoice, PdfExporter("hello.pdf"))


if __name__ == "__main__":
    main()
