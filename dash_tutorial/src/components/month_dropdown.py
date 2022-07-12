import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.source import DataSource
from . import ids
from .dropdown_helper import to_dropdown_options


def render(app: Dash, data: DataSource) -> html.Div:
    @app.callback(
        Output(ids.MONTH_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_MONTHS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_months(years: list[str], _: int) -> list[str]:
        return data.filter(years=years).unique_months

    return html.Div(
        children=[
            html.H6(i18n.t("general.month")),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=to_dropdown_options(data.unique_months),
                value=data.unique_months,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
                id=ids.SELECT_ALL_MONTHS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
