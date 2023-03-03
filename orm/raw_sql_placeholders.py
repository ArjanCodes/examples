import sqlite3


def main() -> None:
    number_of_top_customers = int(
        input("How many top customers do you want to query? ")
    )

    con = sqlite3.connect("database/sample_database.db")

    cur = con.cursor()

    raw_sql = """
	SELECT 
		c.id, 
		c.first_name, 
		SUM(i.total) AS total
	FROM Invoice i 
	LEFT JOIN Customer c ON i.customer_id = c.id
	GROUP BY c.id, c.first_name
	ORDER BY total DESC
	LIMIT :limit;
	"""
    
	placeholder = {
        "limit": number_of_top_customers
	}

    for row in cur.execute(raw_sql, placeholder):
        print(row)


if __name__ == "__main__":
    main()
