import sqlite3

from skypulse.database.database import DATABASE


conn = sqlite3.connect(DATABASE)

cursor = conn.cursor()

# Insert sample data into the employees table
sample_data = [
    ("John Doe", "Software Engineer", 80000.0),
    ("Jane Smith", "Data Scientist", 90000.0),
    ("Bob Johnson", "Project Manager", 95000.0),
    ("Alice Brown", "System Administrator", 85000.0),
    ("Charlie Davis", "Business Analyst", 82000.0),
]

cursor.executemany(
    """
    INSERT INTO employees (name, position, salary)
    VALUES (?, ?, ?)
""",
    sample_data,
)

# Commit changes
conn.commit()

# Close the connection
conn.close()
