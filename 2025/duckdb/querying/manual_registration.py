import duckdb


def main() -> None:
    query = """
        SELECT
            name,
            job_title,
            salary,
        FROM employees
        WHERE salary > 125000
        LIMIT 3
    """

    with duckdb.connect() as conn:
        data = conn.read_csv("data/employees.csv")
        conn.register("employees", data)
        result_df = conn.execute(query).fetchdf()

    # Display the result
    print("3 records with a high salary per year:")
    print(result_df)


if __name__ == "__main__":
    main()
