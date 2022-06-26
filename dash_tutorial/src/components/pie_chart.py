import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.config import SettingsSchema
from src.schema import TransactionsSchema


def render(app: Dash, settings: SettingsSchema) -> html.Div:
    @app.callback(
        Output(settings.components.pie_chart.id, "children"),
        Input(settings.components.records.id, "data"),
    )
    def update_pie_chart(pivot_table_records: list[dict[str, float]]) -> dcc.Graph:
        pivot_table = pd.DataFrame(pivot_table_records)
        pie = go.Pie(
            labels=pivot_table.loc[:, TransactionsSchema.category],
            values=pivot_table.loc[:, TransactionsSchema.amount],
            hole=0.5,
        )
        fig = go.Figure(data=[pie])
        fig.update_layout(margin={"t": 40, "b": 0, "l": 0, "r": 0})
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")
        return dcc.Graph(figure=fig)

    return html.Div(id=settings.components.pie_chart.id)
