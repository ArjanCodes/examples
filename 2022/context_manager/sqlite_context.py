import logging
import sqlite3


class SQLite:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.connection = sqlite3.connect(self.file_name)

    def __enter__(self):
        logging.info("Calling __enter__")
        return self.connection.cursor()

    def __exit__(self, error: Exception, value: object, traceback: object):
        logging.info("Calling __exit__")
        self.connection.commit()
        self.connection.close()


def main():
    logging.basicConfig(level=logging.INFO)
    with SQLite(file_name="application.db") as cursor:
        cursor.execute("SELECT * FROM blogs")
        logging.info(cursor.fetchall())


if __name__ == "__main__":
    main()
