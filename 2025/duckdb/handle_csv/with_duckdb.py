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
                job_title,
                salary,
            FROM employees
            WHERE salary > 125000
            LIMIT 3
        """

        result_df = conn.execute(query).fetchdf()

        print("3 records with a high salary:")
        print(result_df)

        # get the full table as a DataFrame
        full_df = relation.to_df()

        # apply a filter to the DataFrame
        filtered_df = full_df[full_df["salary"] > 125000][
            ["name", "job_title", "salary"]
        ].head(3)
        print("3 records with a high salary:")
        print(filtered_df)


if __name__ == "__main__":
    main()
