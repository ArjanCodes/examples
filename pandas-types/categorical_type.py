from pathlib import Path

import pandas as pd


def read_raw_dataset() -> pd.DataFrame:
    """Reads the Olist e-commerce customers dataset."""
    dataset_path = Path("pandas-types").absolute() / "datasets"
    df = pd.read_csv(dataset_path / "olist_customers_dataset.csv")
    return df


def calculate_memory_usage(df: pd.DataFrame) -> pd.Series:
    """Returns the real memory usage of a DataFrame including object types."""

    memory_usage = df.memory_usage(deep=True)
    print("--- Memory consumption ---")
    print(memory_usage, end="\n\n")

    return memory_usage


def convert_to_categorical(
    df_to_convert: pd.DataFrame, columns: list[str]
) -> pd.DataFrame:
    """Converts all the specified columns of a dataframe to categorical types."""

    df_out = df_to_convert.copy()
    for column in columns:
        df_out[column] = df_out[column].astype("category")

    return df_out


def calculate_percentage_difference(inicial: pd.Series, final: pd.Series) -> pd.Series:
    """Return the percentage difference of two pandas Series."""
    return (final - inicial) / inicial * 100


def main():
    customers_before_type_conversion = read_raw_dataset()
    print("--- Types before conversion ---")
    print(customers_before_type_conversion.dtypes, end="\n\n")

    initial_memory_usage = calculate_memory_usage(customers_before_type_conversion)

    customers_after_type_conversion = convert_to_categorical(
        df_to_convert=customers_before_type_conversion,
        columns=[
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state",
        ],
    )

    print("--- Types after conversion ---")
    print(customers_after_type_conversion.dtypes, end="\n\n")

    final_memory_usage = calculate_memory_usage(customers_after_type_conversion)

    memory_reduction_percent = calculate_percentage_difference(
        inicial=initial_memory_usage, final=final_memory_usage
    )

    print("--- Memory reduction percentage ---")
    print(memory_reduction_percent)


if __name__ == "__main__":
    main()
