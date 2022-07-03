import enum

import pandas as pd


@enum.unique
class DataSchema(enum.Enum):
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"


def load_transaction_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT.value: float,
            DataSchema.CATEGORY.value: str,
            DataSchema.MONTH.value: str,
            DataSchema.YEAR.value: str,
        },
        parse_dates=[DataSchema.DATE.value],
    )
    return data
