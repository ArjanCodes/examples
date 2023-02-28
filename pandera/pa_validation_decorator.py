from pathlib import Path
from typing import Union

import pandas as pd
from altered_schema import schema

import pandera as pa


@pa.check_output(schema, lazy=True)
def retrieve_retail_products(path: Union[Path, str]) -> pd.DataFrame:
    """Read procuts info as a pandas dataframe."""
    return pd.read_csv(path)


def main() -> None:
    dataset_path = Path().absolute() / "datasets"

    products = retrieve_retail_products(dataset_path / "online_retail.csv")

    print(products.head())


if __name__ == "__main__":
    main()
