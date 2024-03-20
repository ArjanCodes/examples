import sqlite3
from typing import Protocol


class DatabaseConnector(Protocol):
    def connect(self, database: str) -> sqlite3.Connection: ...

    def create_cursor(self, conn: sqlite3.Connection) -> sqlite3.Cursor: ...

    def close_connection(self, conn: sqlite3.Connection) -> None: ...


class SQLiteConnector(DatabaseConnector):
    def connect(self, database: str) -> sqlite3.Connection:
        return sqlite3.connect(database)

    def create_cursor(self, conn: sqlite3.Connection) -> sqlite3.Cursor:
        return conn.cursor()

    def close_connection(self, conn: sqlite3.Connection):
        conn.close()
