import duckdb


def main() -> None:
    # Load employees.csv into DuckDB
    conn = duckdb.connect()
    data = conn.read_csv("data/employees.csv")
    conn.register("employees", data)

    # DESCRIBE
    print("\nDESCRIBE:")
    print(conn.sql("DESCRIBE employees"))

    # EXPLAIN
    print("\nEXPLAIN:")
    explain_result = """
        SELECT job_title, AVG(salary) 
        FROM employees 
        WHERE salary > 125000 
        GROUP BY job_title
    """
    print(conn.sql(query=explain_result).explain())

    # # SUMMARIZE
    print("\nSUMMARIZE:")
    print(conn.sql("SUMMARIZE employees"))


if __name__ == "__main__":
    main()
