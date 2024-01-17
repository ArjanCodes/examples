
import sqlite3


def create_city_storms(conn: sqlite3.Connection):
    """ Create table """
    try:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE city_storms (
                            id INTEGER PRIMARY KEY,
                            city_id INTEGER,
                            storm_id INTEGER,
                            FOREIGN KEY (city_id) REFERENCES cities(city_id),
                            FOREIGN KEY (storm_id) REFERENCES storms(storm_id)
                        );
                     """)
    except sqlite3.Error as e:
        print(e)