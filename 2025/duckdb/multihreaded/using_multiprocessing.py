import duckdb
import multiprocessing


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


def query_database(db_path: str, process_name: str, min_salary: int) -> None:
    """Perform a query on the database in a separate process."""
    with duckdb.connect(database=db_path, read_only=True) as conn:
        query = f"""
        SELECT * FROM employees
        WHERE salary > {min_salary}
        """
        result = conn.execute(query).fetchdf()
        print(f"[{process_name}] Employees with salary > {min_salary}:")
        print(result)


def main() -> None:
    # Path to the persistent DuckDB database file
    db_path = "employees_db.duckdb"
    csv_path = "data/employees.csv"

    # Load data into the DuckDB database
    load_data(db_path, csv_path)

    # Define salary thresholds for the queries
    salary_thresholds = [50000, 70000, 90000]

    # Create and manage processes dynamically
    processes: list[multiprocessing.Process] = []
    for i, threshold in enumerate(salary_thresholds):
        process_name = f"Process-{i + 1}"
        process = multiprocessing.Process(
            target=query_database, args=(db_path, process_name, threshold)
        )
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    print("All queries are complete.")


if __name__ == "__main__":
    main()
