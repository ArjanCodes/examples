from pathlib import Path
from typing import Union

import pandas as pd
import pandera as pa


def retrieve_retail_products(path: Union[Path, str]) -> pd.DataFrame:
    """Read procuts info as a pandas dataframe."""
    return pd.read_csv(path)


def main() -> None:
    dataset_path = Path().absolute() / "datasets"

    products = retrieve_retail_products(dataset_path / "online_retail.csv")

    products_infered_schema = pa.infer_schema(products)

    with open("infered_schema.py", "w") as file:
        file.write(products_infered_schema.to_script())

    # Change the infered schema from infered_schema.py according to specifics needs
    # and save it to altered_schema.py
    from altered_schema import schema

    try:
        schema.validate(products, lazy=True)
    except pa.errors.SchemaErrors as err:
        print(err)


if __name__ == "__main__":
    main()
