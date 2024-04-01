import sqlite3
import logging
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO)

class DBConnectionHandler:
    def __init__(self, db_name: str):
        self.db_name: str = db_name
        self.connection: Optional[sqlite3.Connection] = None

    def __enter__(self) -> sqlite3.Connection:
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        assert self.connection is not None
        self.connection.close()

def create_tables() -> None:
    with DBConnectionHandler('example.db') as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        connection.commit()

def drop_tables() -> None:
    with DBConnectionHandler('example.db') as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS items')
        connection.commit()

class Repository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection: sqlite3.Connection = connection

    def add(self, name: str, quantity: int) -> None:
        cursor: sqlite3.Cursor = self.connection.cursor()
        cursor.execute('INSERT INTO items (name, quantity) VALUES (?, ?)', (name, quantity))
        self.connection.commit()

    def all(self) -> List[Dict[str, Any]]:
        cursor: sqlite3.Cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM items')
        return [dict(row) for row in cursor.fetchall()]

class UnitOfWork:
    def __init__(self, db_name: str = 'example.db'):
        self.db_name: str = db_name
        self.connection: Optional[sqlite3.Connection] = None
        self.repository: Optional[Repository] = None

    def __enter__(self) -> 'UnitOfWork':
        self.connection = sqlite3.connect(self.db_name)
        self.connection.execute('BEGIN')
        self.connection.row_factory = sqlite3.Row
        self.repository = Repository(self.connection)
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        assert self.connection is not None
        if exc_val:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

def main() -> None:
    create_tables()

    try:
        with UnitOfWork() as uow:
            assert uow.repository is not None
            uow.repository.add('Apple', 10)
            uow.repository.add('Banana', 20)
            # raise Exception("Something went wrong")
    except Exception as e:
        logging.error(f"Error during database operation: {e}")

    with DBConnectionHandler('example.db') as connection:
        repo: Repository = Repository(connection)
        logging.info("Items in the database:")
        for item in repo.all():
            logging.info(item)

    drop_tables()

if __name__ == '__main__':
    main()
