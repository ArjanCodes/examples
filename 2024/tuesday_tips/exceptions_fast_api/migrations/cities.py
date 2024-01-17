import sqlite3


def create_cities(conn: sqlite3.Connection):
    """ Create cities """
    try:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS cities (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            population INTEGER
                          );
                       """)
    except sqlite3.Error as e:
        print(e)