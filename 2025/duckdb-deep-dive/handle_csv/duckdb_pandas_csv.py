import duckdb
import pandas as pd


def main() -> None:
    _dataframe = pd.read_csv("data/employees.csv")

    query = """
        SELECT
            sum(salary) as total_salary,
        FROM _dataframe
    """

    # Get the value directly
    result = duckdb.query(query)

    # Or return it as a DataFrame
    result_df = duckdb.query(query).fetchdf()

    print("Total salary:")
    print(result)
    print(result_df)


if __name__ == "__main__":
    main()
