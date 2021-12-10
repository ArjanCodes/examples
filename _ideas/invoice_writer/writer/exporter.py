from typing import Protocol

from writer.invoice import Invoice


class Exporter(Protocol):
    def export(self, invoice: Invoice) -> None:
        ...
