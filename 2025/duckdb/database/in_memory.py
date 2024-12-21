import duckdb


def main() -> None:
    with duckdb.connect() as conn:
        # Read data from CSV file
        employees = conn.read_csv("data/employees.csv")

        # Preview data from the employees table
        data = conn.execute("SELECT * FROM employees").fetchdf()
        print(data)


if __name__ == "__main__":
    main()
