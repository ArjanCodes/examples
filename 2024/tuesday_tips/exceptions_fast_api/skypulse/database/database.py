import sqlite3
from typing import Any, AsyncGenerator

DATABASE = "./skypulse/database/skypulse.db"

class NotFoundError(Exception):
    pass

async def setup_db_connection(database: str = DATABASE) -> AsyncGenerator[sqlite3.Cursor, Any]:
    connector = sqlite3.connect(database)
    try: 
        yield connector.cursor()
    finally:
        connector.close()
