from dash import Dash, html
from dash.dependencies import Input, Output

from ..data.source import DataSource
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:
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
        return source.create_bar_chart(years, months, categories, orientation="v")

    return html.Div(id=ids.BAR_CHART)
