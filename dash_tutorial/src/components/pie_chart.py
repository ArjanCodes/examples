import i18n
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.data.loader import DataSchema

from . import ids


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.PIE_CHART, "children"),
        Input(ids.RECORDS, "data"),
    )
    def update_pie_chart(pivot_table_records: list[dict[str, float]]) -> html.Div:
        if len(pivot_table_records) == 0:
            return html.Div(i18n.t("general.no_data"))
        pivot_table = pd.DataFrame(pivot_table_records)
        pie = go.Pie(
            labels=pivot_table.loc[:, DataSchema.CATEGORY.value],
            values=pivot_table.loc[:, DataSchema.AMOUNT.value],
            hole=0.5,
        )
        fig = go.Figure(data=[pie])
        fig.update_layout(margin={"t": 40, "b": 0, "l": 0, "r": 0})
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")
        return html.Div(dcc.Graph(figure=fig))

    return html.Div(id=ids.PIE_CHART)
