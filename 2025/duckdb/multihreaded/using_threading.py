import duckdb
import threading


def load_data(db_path: str, csv_path: str) -> None:
    """Load data from a CSV file into a DuckDB table."""
    with duckdb.connect(database=db_path, read_only=False) as conn:
        # Read data from CSV into a relation
        relation = conn.read_csv(csv_path)

        # Create a table from the relation if it doesn't exist
        conn.execute("CREATE TABLE IF NOT EXISTS employees AS SELECT * FROM relation")

        # Optional: Preview the data
        data = conn.execute("SELECT * FROM employees").fetchdf()
        print("Loaded data preview:")
        print(data)


def query_database(db_path: str, thread_name: str, min_salary: int) -> None:
    """Perform a query on the database in a thread."""
    with duckdb.connect(database=db_path, read_only=True) as conn:
        query = f"""
        SELECT * FROM employees
        WHERE salary > {min_salary}
        """
        result = conn.execute(query).fetchdf()
        print(f"[{thread_name}] Employees with salary > {min_salary}:")
        print(result)


def main() -> None:
    # Path to the persistent DuckDB database file
    db_path = "employees_db.duckdb"
    csv_path = "data/employees.csv"

    # Load data into the DuckDB database
    load_data(db_path, csv_path)

    # Define salary thresholds for the queries
    salary_thresholds = [50000, 70000, 90000]

    # Create and manage threads dynamically
    threads: list[threading.Thread] = []
    for i, threshold in enumerate(salary_thresholds):
        thread_name = f"Thread-{i + 1}"
        thread = threading.Thread(
            target=query_database, args=(db_path, thread_name, threshold)
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All queries are complete.")


if __name__ == "__main__":
    main()
