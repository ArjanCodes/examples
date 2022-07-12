from functools import reduce
from typing import Callable

import i18n
import pandas as pd

Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


class DataSchema:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"


def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.YEAR] = df[DataSchema.DATE].dt.year.astype(str)
    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.MONTH] = df[DataSchema.DATE].dt.month.astype(str)
    return df


def convert_date_locale(
    df: pd.DataFrame,
) -> pd.DataFrame:
    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]

    def date_repr(date_str: str) -> str:
        return i18n.t(f"datetime.{months[int(date_str) - 1]}")
        # date = datetime.strptime(date_str, datetime_fmt)
        # return babel.dates.format_date(date, format=babel_fmt, locale=locale)

    df[DataSchema.MONTH].apply(date_repr)
    return df


def translate_category_language(df: pd.DataFrame) -> pd.DataFrame:
    print("Translate category language")

    def translate(category: str) -> str:
        return i18n.t(f"category.{category}")

    categories: "pd.Series[str]" = df[DataSchema.CATEGORY]
    translated_categories: "pd.Series[str]" = categories.apply(translate)
    df[DataSchema.CATEGORY] = translated_categories
    return df


def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def load_transaction_data(path: str) -> pd.DataFrame:
    # load the data from the CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.CATEGORY: str,
            DataSchema.MONTH: str,
            DataSchema.YEAR: str,
        },
        parse_dates=[DataSchema.DATE],
    )
    preprocessor = compose(
        create_year_column,
        create_month_column,
        convert_date_locale,
        translate_category_language,
    )
    return preprocessor(data)
