import sqlite3
from cities import create_cities

from city_storms import create_city_storms
from storms import create_storms

conn = sqlite3.connect("./skypulse/database/skypulse.db")

create_cities(conn)
create_storms(conn)
create_city_storms(conn)

# Commit the changes
conn.commit()

# Close the connection
conn.close()
