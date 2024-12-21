import duckdb
import pandas as pd


DATA: dict[str, list[int | str]] = {
    "id": [1, 2, 3, 4, 5],
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "age": [25, 30, 35, 40, 22],
    "city": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "salary": [70000, 80000, 120000, 110000, 60000],
}


def main() -> None:
    # Create a sample DataFrame
    df = pd.DataFrame(DATA)

    with duckdb.connect() as conn:
        conn.sql("CREATE TABLE my_table AS SELECT * FROM df")
        conn.sql("INSERT INTO my_table SELECT * FROM df")

    # Execute the query and fetch the result as a DataFrame
    with duckdb.connect() as conn:
        tables = conn.sql("SHOW ALL TABLES")
        print(tables)


if __name__ == "__main__":
    main()
