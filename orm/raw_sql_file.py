import sqlite3
from pathlib import Path

from jinja2 import Template
from pyparsing import Any


def read_sql_query(sql_path: Path, **sql_kwargs: dict[str, Any]) -> str:
    """Parse parameters to a template SQL file."""
    sql_template = Path(sql_path).read_text()
    template = Template(sql_template)
    return template.render(**sql_kwargs)


def main() -> None:
    con = sqlite3.connect("orm/database/sample_database.db")

    cur = con.cursor()

    raw_sql = read_sql_query("orm/sql/top_customers.sql", number_of_top_customers=10)

    for row in cur.execute(raw_sql):
        print(row)


if __name__ == "__main__":
    main()
