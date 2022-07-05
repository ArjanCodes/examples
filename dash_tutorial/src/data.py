import datetime as dt
import enum

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
    s: "pd.Series[str]",
    locale: str = "en",
    datetime_fmt: str = "%m-%b",
    babel_fmt: str = "MM-MMM",
) -> "pd.Series[str]":
    dates: "pd.Series[str]" = s.apply(lambda _: dt.datetime.strptime(_, datetime_fmt))
    converted_dates: "pd.Series[str]" = dates.apply(
        lambda _: babel.dates.format_date(_, format=babel_fmt, locale=locale)
    )
    return converted_dates


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
