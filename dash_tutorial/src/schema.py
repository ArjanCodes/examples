import datetime as dt

import numpy as np
import pandera as pa

from src.config import SETTINGS


class RawTransactionsSchema(pa.SchemaModel):
    date: pa.typing.Series[str]
    amount: pa.typing.Series[float]
    category: pa.typing.Series[str]


class TransactionsSchema(pa.SchemaModel):
    date: pa.typing.Series[np.datetime64]
    amount: pa.typing.Series[float]
    category: pa.typing.Series[str]
    year: pa.typing.Series[str]
    month: pa.typing.Series[str]

    @pa.check(SETTINGS.data.columns.year, name="year_format")
    def check_year_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, SETTINGS.dates.year_format)

    @pa.check(SETTINGS.data.columns.month, name="month_format")
    def check_month_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, SETTINGS.dates.month_format)


def check_date_format(s: pa.typing.Series[str], fmt: str) -> pa.typing.Series[bool]:
    checks = [True if dt.datetime.strptime(_, fmt) else False for _ in s]
    return pa.typing.Series(checks, dtype=bool)
