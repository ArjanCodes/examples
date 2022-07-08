import functools
from dataclasses import dataclass
from typing import Callable, Optional, cast

import numpy as np
import pandas as pd

from .loader import DataSchema

ComposableFunction = Callable[[pd.DataFrame], pd.DataFrame]


def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.YEAR.value] = df[DataSchema.DATE.value].dt.year.astype(str)
    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.MONTH.value] = df[DataSchema.DATE.value].dt.month.astype(str)
    return df


def compose(*functions: ComposableFunction) -> ComposableFunction:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


preprocessor = compose(create_year_column, create_month_column)


@dataclass
class DataSource:
    _data: pd.DataFrame
    _preprocessor: Optional[ComposableFunction] = None

    def __post_init__(self) -> None:
        if self._preprocessor is not None:
            self._data = self._preprocessor(self._data)

    def filter(
        self,
        years: Optional[list[str]] = None,
        months: Optional[list[str]] = None,
        categories: Optional[list[str]] = None,
    ) -> "DataSource":
        year_mask = np.isin(self.all_years, self.all_years if years is None else years)
        month_mask = np.isin(
            self.all_months, self.all_months if months is None else months
        )
        category_mask = np.isin(
            self.all_categories,
            self.all_categories if categories is None else categories,
        )
        mask = year_mask & month_mask & category_mask
        filtered_data = self._data.loc[mask]
        return DataSource(filtered_data)

    @property
    def category_table(self) -> list[dict[str, str | float]]:
        transactions_pivot_table = self._data.pivot_table(
            values=[DataSchema.AMOUNT.value],
            index=[DataSchema.CATEGORY.value],
            aggfunc="sum",
            fill_value=0,
            dropna=False,
        ).reset_index()

        pivot_table_records = transactions_pivot_table.to_dict(orient="records")
        return cast(list[dict[str, str | float]], pivot_table_records)

    @property
    def all_years(self) -> list[str]:
        return self._data[DataSchema.DATE.value].dt.year.astype(str).tolist()

    @property
    def all_months(self) -> list[str]:
        return self._data[DataSchema.DATE.value].dt.month.astype(str).tolist()

    @property
    def all_categories(self) -> list[str]:
        return self._data[DataSchema.CATEGORY.value].tolist()

    @property
    def years(self) -> list[str]:
        return sorted(set(self.all_years), key=int)

    @property
    def months(self) -> list[str]:
        return sorted(set(self.all_months), key=int)

    @property
    def categories(self) -> list[str]:
        return sorted(set(self.all_categories))
