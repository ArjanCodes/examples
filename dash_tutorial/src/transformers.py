import datetime as dt
from typing import Protocol

import pandas as pd
from sklearn import pipeline
from sklearn.base import BaseEstimator, TransformerMixin

from src.config import SETTINGS
from src.schema import DateColumnSchema, MonthColumnSchema, YearColumnSchema


class DateFormats(Protocol):
    date_format: str
    year_format: str
    month_format: str


def create_preprocessing_pipeline() -> pipeline.Pipeline:
    return pipeline.make_pipeline(CreateYearFromDate(), CreateMonthFromDate())


class CreateYearFromDate(BaseEstimator, TransformerMixin):
    def fit(self, x: pd.DataFrame, y=None) -> "CreateYearFromDate":
        DateColumnSchema.validate(x)
        return self

    def transform(self, x: pd.DataFrame, y=None) -> pd.DataFrame:
        _x = x.copy()
        _x.loc[:, YearColumnSchema.year] = (
            _x.loc[:, DateColumnSchema.date]
            .apply(lambda d: dt.datetime.strptime(d, SETTINGS.dates.date_format))
            .apply(lambda d: dt.datetime.strftime(d, SETTINGS.dates.year_format))
        )
        return _x


class CreateMonthFromDate(BaseEstimator, TransformerMixin):
    def fit(self, x: pd.DataFrame, y=None) -> "CreateMonthFromDate":
        DateColumnSchema.validate(x)
        return self

    def transform(self, x: pd.DataFrame, y=None) -> pd.DataFrame:
        _x = x.copy()
        _x.loc[:, MonthColumnSchema.month] = (
            _x.loc[:, DateColumnSchema.date]
            .apply(lambda d: dt.datetime.strptime(d, SETTINGS.dates.date_format))
            .apply(lambda d: dt.datetime.strftime(d, SETTINGS.dates.month_format))
        )
        return _x
