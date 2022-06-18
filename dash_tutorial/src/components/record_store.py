from typing import Any, cast

import dash
import pandas as pd
from dash.dependencies import Input, Output
from src.config import SettingsSchema
from src.schema import TransactionsSchema
from src.transactions import load_transaction_data


def initialize(app: dash.Dash, settings: SettingsSchema) -> None:
    @app.callback(
        Output(settings.components.records.id, "data"),
        [
            Input(settings.components.year_dropdown.id, "value"),
            Input(settings.components.month_dropdown.id, "value"),
            Input(settings.components.category_dropdown.id, "value"),
        ],
    )
    def filter_budget_records(
        years: list[int], months: list[str], categories: list[str]
    ) -> list[dict[str, Any]]:
        transactions = load_transaction_data(settings.data.path)
        year_mask = transactions.isin(years).loc[:, TransactionsSchema.year]
        month_mask = transactions.isin(months).loc[:, TransactionsSchema.month]
        category_mask = transactions.isin(categories).loc[
            :, TransactionsSchema.category
        ]
        row_mask = year_mask & month_mask & category_mask
        filtered_transactions: pd.DataFrame = transactions.loc[row_mask, :]

        transactions_pivot_table = filtered_transactions.pivot_table(
            values=[TransactionsSchema.amount],
            index=[TransactionsSchema.category],
            aggfunc="sum",
            fill_value=0,
            dropna=False,
        ).reset_index()

        pivot_table_records = transactions_pivot_table.to_dict(orient="records")
        return cast(list[dict[str, Any]], pivot_table_records)
