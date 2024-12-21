import duckdb


def main() -> None:
    query = """
        SELECT
            name,
            job_title,
            salary,
        FROM employees
        WHERE salary > 2000
        LIMIT 3
    """
    
    with duckdb.connect() as conn:
        employees = conn.read_csv(
            "data/employees.csv"
        )
        result_df = conn.execute(query).fetchdf()

    print("Top 3 records with the highest salary per year:")
    print(result_df)


if __name__ == "__main__":
    main()
