import duckdb


# Create a sample DataFrame
def main() -> None:
    # Read data from CSV file
    with duckdb.connect() as conn:
        # Create a table and populate it with data from the CSV file
        relation = conn.read_csv("data/employees.csv")

        # Create a table from the relation
        conn.execute("CREATE TABLE employees AS SELECT * FROM relation")

        # Optional: Preview data from the employees table
        data = conn.execute("SELECT * FROM employees").fetchdf()

        print("Preview of the employees table:")
        print(data)


if __name__ == "__main__":
    main()
