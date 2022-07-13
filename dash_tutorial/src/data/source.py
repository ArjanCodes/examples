from dataclasses import dataclass
from typing import Optional

import numpy as np
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
    def data(self) -> pd.DataFrame:
        return self._data

    @property
    def shape(self) -> tuple[int, int]:
        return self._data.shape

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
