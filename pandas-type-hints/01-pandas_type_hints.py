from pathlib import Path

import pandas as pd


def retrieve_retail_products(path: Path | str) -> pd.DataFrame:
    return pd.read_csv(path)


products = retrieve_retail_products("datasets/online_retail.csv")
