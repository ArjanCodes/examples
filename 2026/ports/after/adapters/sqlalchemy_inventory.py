from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.engine import Connection

from ..domain.errors import UnknownSku
from ..domain.models import Sku
from ..domain.ports import InventoryPort


@dataclass
class SqlAlchemyInventoryAdapter(InventoryPort):
    conn: Connection

    def get_stock(self, sku: Sku) -> int:
        row = self.conn.execute(
            text("SELECT stock FROM inventory WHERE sku = :sku"),
            {"sku": str(sku)},
        ).fetchone()

        if row is None:
            raise UnknownSku(str(sku))

        return int(row.stock)

    def reserve(self, sku: Sku, qty: int) -> int:
        # Demo-friendly (not fully concurrent-safe). Kept here on purpose: infra detail.
        self.conn.execute(
            text("UPDATE inventory SET stock = stock - :qty WHERE sku = :sku"),
            {"sku": str(sku), "qty": qty},
        )
        remaining = self.conn.execute(
            text("SELECT stock FROM inventory WHERE sku = :sku"),
            {"sku": str(sku)},
        ).scalar_one()
        return int(remaining)
