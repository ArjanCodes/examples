import duckdb


# Create a sample DataFrame
def main() -> None:
    # Read data from CSV file
    with duckdb.connect() as conn:
        relation = conn.read_csv("data/employees.csv")
        conn.register("employees", relation)

        # Query the DataFrame using DuckDB SQL
        query = """
            SELECT
                name,
                position,
                salary,
            FROM employees
            WHERE salary > 2000
            LIMIT 3
        """

        result_df = conn.execute(query).fetchdf()

    print("Top 3 records with the highest salary per year:")
    print(result_df)


if __name__ == "__main__":
    main()
