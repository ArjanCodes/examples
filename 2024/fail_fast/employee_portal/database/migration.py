import sqlite3

from employee_portal.employees import DATABASE

conn = sqlite3.connect(DATABASE)

cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS employees
                  (id INTEGER PRIMARY KEY, name TEXT, position TEXT, salary REAL)"""
)

conn.commit()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        payment_date DATE,
        amount REAL,
        payment_method TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
    )"""
)

conn.commit()
