import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.source import DataSource
from . import ids
from .dropdown_helper import to_dropdown_options


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.CATEGORY_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_CATEGORIES_BUTTON, "n_clicks"),
        ],
    )
    def select_all_categories(years: list[str], months: list[str], _: int) -> list[str]:
        return source.filter(years=years, months=months).unique_categories

    return html.Div(
        children=[
            html.H6(i18n.t("general.category")),
            dcc.Dropdown(
                id=ids.CATEGORY_DROPDOWN,
                options=to_dropdown_options(source.unique_categories),
                value=source.unique_categories,
                multi=True,
                placeholder=i18n.t("general.select"),
            ),
            html.Button(
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
                id=ids.SELECT_ALL_CATEGORIES_BUTTON,
                n_clicks=0,
            ),
        ],
    )
