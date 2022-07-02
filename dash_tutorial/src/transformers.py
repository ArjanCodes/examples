import pandas as pd

from src.schema import DataSchema


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
    x[DataSchema.DATE.value] = pd.to_datetime(
        x[DataSchema.DATE.value], format="%Y-%m-%d"
    )
    return x


def create_year_from_date(x: pd.DataFrame) -> pd.DataFrame:
    x[DataSchema.YEAR.value] = x[DataSchema.DATE.value].dt.strftime("%Y")
    return x


def create_month_from_date(x: pd.DataFrame) -> pd.DataFrame:
    x[DataSchema.MONTH.value] = x[DataSchema.DATE.value].dt.strftime("%m-%b")
    return x
