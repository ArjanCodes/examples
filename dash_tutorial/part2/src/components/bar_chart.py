from venv import create

import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_years = data[DataSchema.YEAR].tolist()
    all_months = data[DataSchema.MONTH].tolist()
    all_categories = data[DataSchema.CATEGORY].tolist()

    @app.callback(
        Output(ids.BAR_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart(
        years: list[str], months: list[str], categories: list[str]
    ) -> html.Div:
        year_mask = np.isin(all_years, all_years if years is None else years)
        month_mask = np.isin(all_months, all_months if months is None else months)
        category_mask = np.isin(
            all_categories,
            all_categories if categories is None else categories,
        )
        mask = year_mask & month_mask & category_mask
        filtered_data = data.loc[mask]

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.BAR_CHART)

        x = "category"
        y = "amount"

        def create_pivot_table() -> pd.DataFrame:
            pt = filtered_data.pivot_table(
                values=DataSchema.AMOUNT,
                index=[DataSchema.CATEGORY],
                aggfunc="sum",
                fill_value=0,
                dropna=False,
            )
            return pt.reset_index().sort_values(DataSchema.AMOUNT, ascending=False)

        fig = px.bar(
            create_pivot_table(),
            x=x,
            y=y,
            color="category",
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
