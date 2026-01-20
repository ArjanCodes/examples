from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy.engine import Connection

from .adapters.sqlalchemy_inventory import SqlAlchemyInventoryAdapter
from .db import engine
from .domain.ports import InventoryPort


def get_conn() -> Iterator[Connection]:
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()


def get_inventory_port() -> Iterator[InventoryPort]:
    # This is the "composition root" for this dependency:
    # - open SQLAlchemy connection
    # - create the adapter
    # - yield it as the port (interface)
    for conn in get_conn():
        yield SqlAlchemyInventoryAdapter(conn)
