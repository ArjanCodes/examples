import pandas as pd
import duckdb


# Create a sample DataFrame
def main() -> None:
    # Read data from CSV file
    data = pd.read_csv("employess.csv")  # type: ignore

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
        conn.register("employees", data)
        result_df = conn.execute(query).fetchdf()

    # Display the result
    print("Top 3 records with the highest salary per year:")
    print(result_df)


if __name__ == "__main__":
    main()
