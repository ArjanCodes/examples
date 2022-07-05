from typing import Callable

import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from . import ids
from .dropdown_helper import to_dropdown_options

MonthReader = Callable[[list[str] | None], list[str]]


def render(app: Dash, month_reader: MonthReader) -> html.Div:
    all_months = month_reader(None)

    @app.callback(
        Output(ids.MONTH_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_MONTHS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_months(years: list[str], _: int) -> list[str]:
        return month_reader(years)

    return html.Div(
        children=[
            html.H6(i18n.t("general.month")),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=to_dropdown_options(all_months),
                value=all_months,
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
