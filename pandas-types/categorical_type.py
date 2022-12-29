from pathlib import Path

import pandas as pd

dataset_path = Path("pandas-types").absolute() / "datasets"

customers_before_type_conversion = pd.read_csv(
    dataset_path / "olist_customers_dataset.csv"
)

print(customers_before_type_conversion.dtypes)

initial_memory_usage = customers_before_type_conversion.memory_usage(deep=True)

categorical_columns = ["customer_zip_code_prefix", "customer_city", "customer_state"]

customers_after_type_conversion = customers_before_type_conversion.copy()

for column in categorical_columns:
    customers_after_type_conversion[column] = customers_after_type_conversion[
        column
    ].astype("category")

print(customers_after_type_conversion.dtypes)

final_memory_usage = customers_after_type_conversion.memory_usage(deep=True)

memory_reduction_percent = (
    (final_memory_usage - initial_memory_usage) / initial_memory_usage * 100
)

print(memory_reduction_percent)
