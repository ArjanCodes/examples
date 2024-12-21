import duckdb
import pandas as pd

df = pd.DataFrame({"value": [10, 20, 30, 40, 50]})
result = duckdb.query("SELECT AVG(value) AS avg_value FROM df").to_df()
print(result)
