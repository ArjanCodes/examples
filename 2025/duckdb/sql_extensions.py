import duckdb

# Load employees.csv into DuckDB
conn = duckdb.connect()
# conn.sql("CREATE TABLE employees AS SELECT * FROM read_csv_auto('employees.csv')")
data = conn.read_csv("data/employees.csv")
conn.register("employees", data)

# DESCRIBE
print(conn.sql("DESCRIBE SELECT name, job_title, salary FROM employees").describe())

# EXPLAIN
print("\nEXPLAIN:")
explain_result ="""
    SELECT job_title, AVG(salary) 
    FROM employees 
    WHERE salary > 5000 
    GROUP BY job_title
"""
print(conn.sql(query=explain_result).explain())


# SUMMARIZE
print("\nSUMMARIZE:")
print(conn.sql("SUMMARIZE employees").fetchdf())
