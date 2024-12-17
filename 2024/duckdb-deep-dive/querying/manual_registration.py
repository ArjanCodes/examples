import duckdb


# Create a sample DataFrame
def main() -> None:
    # Query the DataFrame using DuckDB SQL
    query = """
        SELECT
            name,
            position,
            salary,
        FROM employees
        WHERE salary > 1000000
        LIMIT 3
    """

    with duckdb.connect() as conn:
        data = conn.read_csv("data/employees.csv")
        conn.register("employees", data)
        result_df = conn.execute(query).fetchdf()

    # Display the result
    print("Top 3 records with the highest salary per year:")
    print(result_df)


if __name__ == "__main__":
    main()
