import logging
import sqlite3
from contextlib import contextmanager


@contextmanager
def open_db(file_name: str):
    conn = None
    try:
        logging.info("Creating connection")
        conn = sqlite3.connect(file_name)
        yield conn.cursor()
    finally:
        logging.info("Closing connection")
        if conn:
            conn.close()


def main():
    logging.basicConfig(level=logging.INFO)
    with open_db(file_name="application.db") as cursor:
        cursor.execute("SELECT * FROM blogs")
        logging.info(cursor.fetchall())


if __name__ == "__main__":
    main()
