import sqlite3
from pathlib import Path


def read_sql_query(sql_path: str) -> str:
    """Read SQL file as string."""
    return Path(sql_path).read_text()


def main() -> None:
    con = sqlite3.connect("database/sample_database.db")

    number_of_top_customers = int(
        input("How many top customers do you want to query? ")
    )

    cur = con.cursor()

    raw_sql = read_sql_query("sql/top_customers.sql")

    placeholder = {"limit": number_of_top_customers}

    for row in cur.execute(raw_sql, placeholder):
        print(row)


if __name__ == "__main__":
    main()
