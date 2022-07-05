import pandas as pd

from .loader import DataSchema


def get_uniques(data: pd.DataFrame, col: str) -> list[str]:
    values: "pd.Series[str]" = data[col]
    return list(set(values))


def get_year_values(data: pd.DataFrame) -> list[str]:
    return get_uniques(data, DataSchema.YEAR.value)
