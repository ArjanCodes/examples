import sqlite3


def create_storms(conn: sqlite3.Connection):
    """ Create storms """
    try:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS storms (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            population INTEGER
                          )
                       ;""")
    except sqlite3.Error as e:
        print(e)