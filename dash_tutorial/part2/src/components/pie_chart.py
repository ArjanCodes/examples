import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_years = data[DataSchema.YEAR].tolist()
    all_months = data[DataSchema.MONTH].tolist()
    all_categories = data[DataSchema.CATEGORY].tolist()

    @app.callback(
        Output(ids.PIE_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_pie_chart(
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
            return html.Div("No data selected.", id=ids.PIE_CHART)

        pie = go.Pie(
            labels=filtered_data[DataSchema.CATEGORY].tolist(),
            values=filtered_data[DataSchema.AMOUNT].tolist(),
            hole=0.5,
        )

        fig = go.Figure(data=[pie])
        fig.update_layout(margin={"t": 40, "b": 0, "l": 0, "r": 0})
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")

        return html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART)

    return html.Div(id=ids.PIE_CHART)
