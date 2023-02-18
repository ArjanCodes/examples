import sqlite3

con = sqlite3.connect(r"orm\database\sample_database.db")

cur = con.cursor()

number_of_top_customers = 10

raw_sql = f"""
SELECT 
	c.id, 
	c.first_name, 
	SUM(i.total) AS total
FROM Invoice i 
LEFT JOIN Customer c ON i.customer_id = c.id
GROUP BY c.id, c.first_name
ORDER BY total DESC
LIMIT {number_of_top_customers};
"""

for row in cur.execute(raw_sql):
    print(row)
