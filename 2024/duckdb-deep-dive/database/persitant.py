import duckdb


def main() -> None:
    # Path to the persistent DuckDB database file
    db_path = "employees_db.duckdb"

    # Connect to DuckDB (creates or opens the specified database file)
    with duckdb.connect(database=db_path, read_only=False) as conn:
        # Read data from CSV file into a relation
        relation = conn.read_csv("data/employees.csv")

        # Create a table from the relation (if it doesn't exist)
        conn.execute("CREATE TABLE IF NOT EXISTS employees AS SELECT * FROM relation")

        # Optional: Preview data from the employees table
        data = conn.execute("SELECT * FROM employees").fetchdf()
        print("Preview of the employees table:")
        print(data)


if __name__ == "__main__":
    main()
