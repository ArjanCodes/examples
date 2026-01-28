from dataclasses import dataclass

from domain.ports import InventoryPort
from sqlalchemy import text
from sqlalchemy.engine import Connection


@dataclass
class SqlAlchemyInventoryAdapter(InventoryPort):
    conn: Connection

    def exists_sku(self, sku: str) -> bool:
        row = self.conn.execute(
            text("SELECT 1 FROM inventory WHERE sku = :sku"),
            {"sku": sku},
        ).fetchone()

        return row is not None

    def get_stock(self, sku: str) -> int:
        row = self.conn.execute(
            text("SELECT stock FROM inventory WHERE sku = :sku"),
            {"sku": sku},
        ).fetchone()

        return int(row.stock)

    def reserve(self, sku: str, qty: int) -> int:
        self.conn.execute(
            text("UPDATE inventory SET stock = stock - :qty WHERE sku = :sku"),
            {"sku": sku, "qty": qty},
        )
        remaining = self.conn.execute(
            text("SELECT stock FROM inventory WHERE sku = :sku"),
            {"sku": sku},
        ).scalar_one()

        self.conn.commit()

        return int(remaining)
