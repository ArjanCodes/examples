import sqlite3

con = sqlite3.connect(r"orm\database\sample_database.db")

cur = con.cursor()

number_of_top_customers = 10

raw_sql = f"""
SELECT 
	c.CustomerId, 
	c.FirstName, 
	SUM(i.Total) AS Total
FROM Invoice i 
LEFT JOIN Customer c ON i.CustomerId = c.CustomerId
GROUP BY c.CustomerId, c.FirstName
ORDER BY TOTAL DESC
LIMIT {number_of_top_customers};
"""

for row in cur.execute(raw_sql):
    print(row)
