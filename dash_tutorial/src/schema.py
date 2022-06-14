import datetime as dt

import pandera as pa

import src

SETTINGS = src.config.load_settings()


class RawTransactionsSchema(pa.SchemaModel):
    date: pa.typing.Series[str]
    amount: pa.typing.Series[float]
    category: pa.typing.Series[str] = pa.Field(nullable=True)


class DateColumnSchema(pa.SchemaModel):
    date: pa.typing.Series[str]

    @pa.check(SETTINGS.data.columns.date, name="date_format")
    def check_date_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[bool]:
        return check_date_format(s, SETTINGS.dates.date_format)


class YearColumnSchema(pa.SchemaModel):
    year: pa.typing.Series[str]

    @pa.check(SETTINGS.data.columns.year, name="year_format")
    def check_year_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, SETTINGS.dates.year_format)


class MonthColumnSchema(pa.SchemaModel):
    month: pa.typing.Series[str]

    @pa.check(SETTINGS.data.columns.month, name="month_format")
    def check_month_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, SETTINGS.dates.month_format)


class TransactionsSchema(pa.SchemaModel):
    date: pa.typing.Series[str]
    amount: pa.typing.Series[float]
    category: pa.typing.Series[str] = pa.Field(nullable=True)
    year: pa.typing.Series[str]
    month: pa.typing.Series[str]

    @pa.check(SETTINGS.data.columns.date, name="date_format")
    def check_date(cls, s: pa.typing.Series[str]) -> pa.typing.Series[bool]:
        return check_date_format(s, SETTINGS.dates.date_format)

    @pa.check(SETTINGS.data.columns.year, name="year_format")
    def check_year_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, SETTINGS.dates.year_format)

    @pa.check(SETTINGS.data.columns.month, name="month_format")
    def check_month_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, SETTINGS.dates.month_format)


def check_date_format(s: pa.typing.Series[str], fmt: str) -> pa.typing.Series[bool]:
    checks = [True if dt.datetime.strptime(_, fmt) else False for _ in s]
    return pa.typing.Series(checks, dtype=bool)
