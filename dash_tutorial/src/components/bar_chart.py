import i18n
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.config import SettingsSchema

from . import ids


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        Input(ids.RECORDS, "data"),
    )
    def update_bar_chart(pivot_table_records: list[dict[str, float]]) -> dcc.Graph:
        print(pivot_table_records)
        pivot_table = pd.DataFrame(pivot_table_records).sort_values(
            "amount", ascending=False
        )
        fig = px.bar(
            pivot_table,
            x="amount",
            y="category",
            color="category",
            orientation="h",
            labels={
                "category": i18n.t("general.category"),
                "amount": i18n.t("general.amount"),
            },
        )
        return dcc.Graph(figure=fig)

    return html.Div(id=ids.BAR_CHART)
