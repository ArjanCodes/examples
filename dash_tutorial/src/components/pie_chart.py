from dash import Dash, html
from dash.dependencies import Input, Output

from ..data.source import DataSource
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:
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
        return source.create_pie_chart(years, months, categories, hole_fraction=0.5)

    return html.Div(id=ids.PIE_CHART)
