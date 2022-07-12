import i18n
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.source import DataSource
from . import ids


def render(app: Dash, source: DataSource, orientation: str = "v") -> html.Div:
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
        filtered_source = source.filter(years, months, categories)
        if filtered_source.shape[0] == 0:
            return html.Div(i18n.t("general.no_data"), id=ids.BAR_CHART)

        x = "amount"
        y = "category"
        if orientation == "v":
            x, y = y, x

        fig = px.bar(
            filtered_source.create_pivot_table(),
            x=x,
            y=y,
            color="category",
            orientation=orientation,
            labels={
                "category": i18n.t("general.category"),
                "amount": i18n.t("general.amount"),
            },
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
