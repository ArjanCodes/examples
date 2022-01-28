import logging
import sqlite3


def main():
    logging.basicConfig(level=logging.INFO)
    connection = sqlite3.connect("application.db")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM blogs")
        logging.info(cursor.fetchall())
    finally:
        connection.close()


if __name__ == "__main__":
    main()
