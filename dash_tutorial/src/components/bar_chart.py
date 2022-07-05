import i18n
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.data.loader import DataSchema

from . import ids


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        Input(ids.RECORDS, "data"),
    )
    def update_bar_chart(pivot_table_records: list[dict[str, float]]) -> html.Div:
        if len(pivot_table_records) == 0:
            return html.Div(i18n.t("general.no_data"))
        pivot_table = pd.DataFrame(pivot_table_records).sort_values(
            DataSchema.AMOUNT.value, ascending=False
        )
        fig = px.bar(
            pivot_table,
            x=DataSchema.AMOUNT.value,
            y=DataSchema.CATEGORY.value,
            color=DataSchema.CATEGORY.value,
            orientation="h",
            labels={
                DataSchema.CATEGORY.value: i18n.t("general.category"),
                DataSchema.AMOUNT.value: i18n.t("general.amount"),
            },
        )
        return html.Div(dcc.Graph(figure=fig))

    return html.Div(id=ids.BAR_CHART)
