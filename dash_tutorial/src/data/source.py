import functools
from dataclasses import dataclass
from typing import Callable, Literal, Optional, cast

import i18n
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html

from ..data.loader import DataSchema
from .loader import DataSchema

ComposableFunction = Callable[[pd.DataFrame], pd.DataFrame]


def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.YEAR.value] = df[DataSchema.DATE.value].dt.year.astype(str)
    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.MONTH.value] = df[DataSchema.DATE.value].dt.month.astype(str)
    return df


def translate_category_language(df: pd.DataFrame) -> pd.DataFrame:
    # df[DataSchema.CATEGORY.value] = df[DataSchema.CATEGORY.value]
    return df


def compose(*functions: ComposableFunction) -> ComposableFunction:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


preprocessor = compose(
    create_year_column, create_month_column, translate_category_language
)


@dataclass
class DataSource:
    _data: pd.DataFrame
    _preprocessor: Optional[ComposableFunction] = None

    def __post_init__(self) -> None:
        if self._preprocessor is not None:
            self._data = self._preprocessor(self._data)

    def create_pie_chart(
        self,
        years: list[str],
        months: list[str],
        categories: list[str],
        hole_fraction: float = 0.5,
    ) -> html.Div:
        filtered_source = self.filter(years, months, categories)
        if filtered_source.shape[0] == 0:
            return html.Div(i18n.t("general.no_data"))

        pie = go.Pie(
            labels=filtered_source.all_categories,
            values=filtered_source.all_amounts,
            hole=hole_fraction,
        )

        fig = go.Figure(data=[pie])
        fig.update_layout(margin={"t": 40, "b": 0, "l": 0, "r": 0})
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")

        return html.Div(dcc.Graph(figure=fig))

    def create_bar_chart(
        self,
        years: list[str],
        months: list[str],
        categories: list[str],
        orientation: Literal["h", "v"] = "h",
    ) -> html.Div:
        # TODO: repeated code to return no data
        filtered_source = self.filter(years, months, categories)
        if filtered_source.shape[0] == 0:
            return html.Div(i18n.t("general.no_data"))

        x = DataSchema.AMOUNT.value
        y = DataSchema.CATEGORY.value
        if orientation == "v":
            x, y = y, x

        fig = px.bar(
            filtered_source.create_pivot_table(),
            x=x,
            y=y,
            color=DataSchema.CATEGORY.value,
            orientation=orientation,
            labels={
                DataSchema.CATEGORY.value: i18n.t("general.category"),
                DataSchema.AMOUNT.value: i18n.t("general.amount"),
            },
        )
        return html.Div(dcc.Graph(figure=fig))

    def create_pivot_table(self) -> pd.DataFrame:
        pt = self._data.pivot_table(
            values=[DataSchema.AMOUNT.value],
            index=[DataSchema.CATEGORY.value],
            aggfunc="sum",
            fill_value=0,
            dropna=False,
        )
        return pt.reset_index().sort_values(DataSchema.AMOUNT.value, ascending=False)

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
    def data(self) -> pd.DataFrame:
        return self._data

    @property
    def shape(self) -> tuple[int, int]:
        return self._data.shape

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
    def all_amounts(self) -> list[str]:
        return self._data[DataSchema.AMOUNT.value].tolist()

    @property
    def years(self) -> list[str]:
        return sorted(set(self.all_years), key=int)

    @property
    def months(self) -> list[str]:
        return sorted(set(self.all_months), key=int)

    @property
    def categories(self) -> list[str]:
        return sorted(set(self.all_categories))
