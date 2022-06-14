import datetime as dt

import pandas as pd
from sklearn import pipeline
from sklearn.base import BaseEstimator, TransformerMixin

import src

SETTINGS = src.config.load_settings()


def create_preprocessing_pipeline() -> pipeline.Pipeline:
    return pipeline.make_pipeline(CreateYearFromDate(), CreateMonthFromDate())


class CreateYearFromDate(BaseEstimator, TransformerMixin):
    def fit(self, x: pd.DataFrame, y=None) -> "CreateYearFromDate":
        src.schema.DateColumnSchema.validate(x)
        return self

    def transform(self, x: pd.DataFrame, y=None) -> pd.DataFrame:
        _x = x.copy()
        _x.loc[:, src.schema.YearColumnSchema.year] = (
            _x.loc[:, src.schema.DateColumnSchema.date]
            .apply(lambda d: dt.datetime.strptime(d, SETTINGS.dates.date_format))
            .apply(lambda d: dt.datetime.strftime(d, SETTINGS.dates.year_format))
        )
        return _x


class CreateMonthFromDate(BaseEstimator, TransformerMixin):
    def fit(self, x: pd.DataFrame, y=None) -> "CreateMonthFromDate":
        src.schema.DateColumnSchema.validate(x)
        return self

    def transform(self, x: pd.DataFrame, y=None) -> pd.DataFrame:
        _x = x.copy()
        _x.loc[:, src.schema.MonthColumnSchema.month] = (
            _x.loc[:, src.schema.DateColumnSchema.date]
            .apply(lambda d: dt.datetime.strptime(d, SETTINGS.dates.date_format))
            .apply(lambda d: dt.datetime.strftime(d, SETTINGS.dates.month_format))
        )
        return _x
