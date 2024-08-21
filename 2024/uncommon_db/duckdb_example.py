import duckdb
import numpy as np
import pandas as pd

# Example 1: Querying Data Directly from CSV without Loading into Memory
duckdb.execute("""
CREATE TABLE employees AS SELECT * FROM 'employees.csv';
""")
result = duckdb.execute("SELECT COUNT(*) FROM employees").fetchall()
print(f"Total number of employees: {result[0][0]}")

# Example 2: Integrating DuckDB with Pandas DataFrame
df = pd.DataFrame(
    {
        "employee_id": range(1, 101),
        "name": [f"Employee {i}" for i in range(1, 101)],
        "salary": np.random.randint(50000, 150000, size=100),
    }
)

# Create a DuckDB table from the DataFrame
duckdb.execute("CREATE TABLE df_employees AS SELECT * FROM df")

# Perform a query directly on the DataFrame
high_earners = duckdb.query_df(df, "df", "SELECT * FROM df WHERE salary > 100000").df()
print("High earners:")
print(high_earners)

# Example 3: Using Window Functions for Analytical Queries
window_query = """
SELECT
    employee_id,
    salary,
    AVG(salary) OVER () AS avg_salary,
    RANK() OVER (ORDER BY salary DESC) AS rank
FROM
    df_employees
"""

ranked_salaries = duckdb.execute(window_query).df()
print("Ranked salaries with average:")
print(ranked_salaries)

# Example 4: Joining Tables and Complex Aggregations
department_df = pd.DataFrame(
    {
        "employee_id": range(1, 101),
        "department": np.random.choice(
            ["Engineering", "HR", "Sales", "Marketing"], size=100
        ),
    }
)

duckdb.execute("CREATE TABLE departments AS SELECT * FROM department_df")

# Perform a join and aggregation
aggregation_query = """
SELECT
    d.department,
    COUNT(e.employee_id) AS num_employees,
    AVG(e.salary) AS avg_salary
FROM
    df_employees e
JOIN
    departments d
ON
    e.employee_id = d.employee_id
GROUP BY
    d.department
"""

department_stats = duckdb.execute(aggregation_query).df()
print("Department statistics:")
print(department_stats)
