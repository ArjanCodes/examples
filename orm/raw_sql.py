import sqlite3


def main() -> None:
    con = sqlite3.connect("database/sample_database.db")

    cur = con.cursor()

    number_of_top_customers = (10,)

    raw_sql = """
	SELECT 
		c.id, 
		c.first_name, 
		SUM(i.total) AS total
	FROM Invoice i 
	LEFT JOIN Customer c ON i.customer_id = c.id
	GROUP BY c.id, c.first_name
	ORDER BY total DESC
	LIMIT ?;
	"""

    for row in cur.execute(raw_sql, number_of_top_customers):
        print(row)


if __name__ == "__main__":
    main()
