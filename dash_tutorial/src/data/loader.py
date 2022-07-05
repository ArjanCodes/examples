import enum
from datetime import datetime

import babel.dates
import pandas as pd


@enum.unique
class DataSchema(enum.Enum):
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"


def convert_locale(
    dates: "pd.Series[str]",
    locale: str = "en",
    datetime_fmt: str = "%m-%b",
    babel_fmt: str = "MM-MMM",
) -> "pd.Series[str]":
    def date_repr(date_str: str) -> str:
        date = datetime.strptime(date_str, datetime_fmt)
        return babel.dates.format_date(date, format=babel_fmt, locale=locale)

    return dates.apply(date_repr)


def load_transaction_data(path: str, locale: str) -> pd.DataFrame:
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
    data[DataSchema.MONTH.value] = convert_locale(data[DataSchema.MONTH.value], locale)
    return data
