import dash
import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from dash.dependencies import Input, Output
from src.config import SettingsSchema
from src.schema import RawTransactionsSchema


def initialize(app: dash.Dash, settings: SettingsSchema) -> None:
    @app.callback(
        Output(settings.components.pie.id, "children"),
        Input(settings.components.records.id, "data"),
    )
    def update_pie_chart(pivot_table_records: list[dict[str, float]]) -> dcc.Graph:
        pivot_table = pd.DataFrame(pivot_table_records)
        pie = go.Pie(
            labels=pivot_table.loc[:, RawTransactionsSchema.category],
            values=pivot_table.loc[:, RawTransactionsSchema.amount],
            hole=0.5,
        )
        fig = go.Figure(data=[pie])
        fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")
        return dcc.Graph(figure=fig)
