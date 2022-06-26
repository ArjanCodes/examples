import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.config import SettingsSchema
from src.schema import TransactionsSchema


def render(app: Dash, settings: SettingsSchema) -> html.Div:
    @app.callback(
        Output(settings.components.bar_chart.id, "children"),
        Input(settings.components.records.id, "data"),
    )
    def update_bar_chart(pivot_table_records: list[dict[str, float]]) -> dcc.Graph:
        pivot_table = pd.DataFrame(pivot_table_records).sort_values(
            "amount", ascending=False
        )
        fig = px.bar(
            pivot_table,
            x=TransactionsSchema.amount,
            y=TransactionsSchema.category,
            color=TransactionsSchema.category,
            orientation="h",
        )
        return dcc.Graph(figure=fig)

    return html.Div(id=settings.components.bar_chart.id)
