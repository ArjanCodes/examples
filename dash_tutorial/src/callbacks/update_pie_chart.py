import dash
import pandas as pd
import plotly.graph_objects as go
import src
from dash import dcc
from dash.dependencies import Input, Output

SETTINGS = src.config.load_settings()


def register(app: dash.Dash) -> None:
    @app.callback(
        Output(SETTINGS.components.pie.id, "children"),
        Input(SETTINGS.components.records.id, "data"),
    )
    def _update_pie_chart(pivot_table_records: list[dict[str, float]]) -> dcc.Graph:
        pivot_table = pd.DataFrame(pivot_table_records)
        pie = go.Pie(
            labels=pivot_table.loc[:, src.schema.RawTransactionsSchema.category],
            values=pivot_table.loc[:, src.schema.RawTransactionsSchema.amount],
            hole=0.5,
        )
        fig = go.Figure(data=[pie])
        fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")
        return dcc.Graph(figure=fig)
