from typing import Any, cast

import dash
import pandas as pd
import src
from dash.dependencies import Input, Output

SETTINGS = src.config.load_settings()


def register(app: dash.Dash) -> None:
    @app.callback(
        Output(SETTINGS.components.records.id, "data"),
        [
            Input(SETTINGS.components.year_dropdown.id, "value"),
            Input(SETTINGS.components.month_dropdown.id, "value"),
            Input(SETTINGS.components.category_dropdown.id, "value"),
        ],
    )
    def _filter_budget_records(
        years: list[int], months: list[str], categories: list[str]
    ) -> list[dict[str, Any]]:
        transactions = src.transactions.load_transaction_data()
        year_mask = transactions.isin(years).loc[:, src.schema.TransactionsSchema.year]
        month_mask = transactions.isin(months).loc[:, src.schema.TransactionsSchema.month]
        category_mask = transactions.isin(categories).loc[:, src.schema.TransactionsSchema.category]
        row_mask = year_mask & month_mask & category_mask
        filtered_transactions: pd.DataFrame = transactions.loc[row_mask, :]

        transactions_pivot_table = filtered_transactions.pivot_table(
            values=[src.schema.TransactionsSchema.amount],
            index=[src.schema.TransactionsSchema.category],
            aggfunc="sum",
            fill_value=0,
            dropna=False,
        ).reset_index()

        pivot_table_records = transactions_pivot_table.to_dict(orient="records")
        return cast(list[dict[str, Any]], pivot_table_records)
