import dash
import pandas as pd
from dash.dependencies import Input, Output

from ..data.source import DataSource
from . import ids


def initialize(app: dash.Dash, data: DataSource) -> None:
    @app.callback(
        Output(ids.RECORDS, "data"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def filter_budget_records(
        years: list[str], months: list[str], categories: list[str]
    ) -> list[dict[str, str | float]]:
        return data.filter(years, months, categories).category_table
