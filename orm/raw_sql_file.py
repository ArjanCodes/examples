import sqlite3
from pathlib import Path


def read_sql_query(sql_path: Path) -> str:
    """Read SQL file as string."""
    return Path(sql_path).read_text()


def main() -> None:
    con = sqlite3.connect("database/sample_database.db")

    number_of_top_customers = (10,)
    cur = con.cursor()

    raw_sql = read_sql_query("sql/top_customers.sql")

    for row in cur.execute(raw_sql, number_of_top_customers):
        print(row)


if __name__ == "__main__":
    main()
