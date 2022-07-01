import locale

import pandas as pd

from src.schema import TransactionsSchema


def preprocessing_pipeline(x: pd.DataFrame) -> pd.DataFrame:
    return (
        x.pipe(copy_dateframe)
        .pipe(convert_to_datetime)
        .pipe(create_year_from_date)
        .pipe(create_month_from_date)
    )


def copy_dateframe(x: pd.DataFrame) -> pd.DataFrame:
    return x.copy()


def convert_to_datetime(x: pd.DataFrame) -> pd.DataFrame:
    x[TransactionsSchema.date] = pd.to_datetime(
        x[TransactionsSchema.date], format="%Y-%m-%d"
    )
    return x


def create_year_from_date(x: pd.DataFrame) -> pd.DataFrame:
    x[TransactionsSchema.year] = x[TransactionsSchema.date].dt.strftime("%Y")
    return x


def create_month_from_date(x: pd.DataFrame) -> pd.DataFrame:
    # I'm struggling with how to properly localize dates...
    date_format = locale.nl_langinfo(locale.D_FMT)
    x[TransactionsSchema.month] = x[TransactionsSchema.date].dt.strftime("%m-%b")
    return x
