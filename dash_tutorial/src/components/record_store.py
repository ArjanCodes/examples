from typing import cast

import dash
import pandas as pd
from dash.dependencies import Input, Output
from src.data.loader import DataSchema
from src.data.manager import DataManager

from . import ids


def initialize(app: dash.Dash, data_manager: DataManager) -> None:
    @app.callback(
        Output(ids.RECORDS, "data"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def filter_budget_records(
        years: list[int], months: list[str], categories: list[str]
    ) -> list[dict[str, str | float]]:
        year_mask: pd.Series = data_manager._data[DataSchema.YEAR.value].isin(years)
        month_mask: pd.Series = data_manager._data[DataSchema.MONTH.value].isin(months)
        category_mask: pd.Series = data_manager._data[DataSchema.CATEGORY.value].isin(
            categories
        )
        row_mask = year_mask & month_mask & category_mask
        filtered_transactions: pd.DataFrame = data_manager._data.loc[row_mask, :]

        transactions_pivot_table = filtered_transactions.pivot_table(
            values=[DataSchema.AMOUNT.value],
            index=[DataSchema.CATEGORY.value],
            aggfunc="sum",
            fill_value=0,
            dropna=False,
        ).reset_index()

        pivot_table_records = transactions_pivot_table.to_dict(orient="records")
        return cast(list[dict[str, str | float]], pivot_table_records)
