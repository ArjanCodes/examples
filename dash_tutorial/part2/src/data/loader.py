import pandas as pd


class DataSchema:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"


def load_transaction_data(path: str) -> pd.DataFrame:
    # load the data from the CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.CATEGORY: str,
            DataSchema.DATE: str,
        },
        parse_dates=[DataSchema.DATE],
    )
    data[DataSchema.YEAR] = data[DataSchema.DATE].dt.year.astype(str)
    data[DataSchema.MONTH] = data[DataSchema.DATE].dt.month.astype(str)
    return data
