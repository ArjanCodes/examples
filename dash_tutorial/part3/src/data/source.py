from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from ..data.loader import DataSchema
from .loader import DataSchema


@dataclass
class DataSource:
    _data: pd.DataFrame

    def filter(
        self,
        years: Optional[list[str]] = None,
        months: Optional[list[str]] = None,
        categories: Optional[list[str]] = None,
    ) -> DataSource:
        if years is None:
            years = self.unique_years
        if months is None:
            months = self.unique_months
        if categories is None:
            categories = self.unique_categories
        filtered_data = self._data.query(
            "year in @years and month in @months and category in @categories"
        )
        return DataSource(filtered_data)

    def create_pivot_table(self) -> pd.DataFrame:
        pt = self._data.pivot_table(
            values=DataSchema.AMOUNT,
            index=[DataSchema.CATEGORY],
            aggfunc="sum",
            fill_value=0,
            dropna=False,
        )
        return pt.reset_index().sort_values(DataSchema.AMOUNT, ascending=False)

    @property
    def row_count(self) -> int:
        return self._data.shape[0]

    @property
    def all_years(self) -> list[str]:
        return self._data[DataSchema.YEAR].tolist()

    @property
    def all_months(self) -> list[str]:
        return self._data[DataSchema.MONTH].tolist()

    @property
    def all_categories(self) -> list[str]:
        return self._data[DataSchema.CATEGORY].tolist()

    @property
    def all_amounts(self) -> list[str]:
        return self._data[DataSchema.AMOUNT].tolist()

    @property
    def unique_years(self) -> list[str]:
        return sorted(set(self.all_years), key=int)

    @property
    def unique_months(self) -> list[str]:
        return sorted(set(self.all_months))

    @property
    def unique_categories(self) -> list[str]:
        return sorted(set(self.all_categories))
