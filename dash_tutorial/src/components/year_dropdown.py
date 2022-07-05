from typing import Callable

import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from . import ids
from .dropdown_helper import to_dropdown_options

YearReader = Callable[[], list[str]]


def render(app: Dash, year_reader: YearReader) -> html.Div:
    year_values = year_reader()

    @app.callback(
        Output(ids.YEAR_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_YEARS_BUTTON, "n_clicks"),
    )
    def select_all_years(_: int) -> list[str]:
        return year_values

    return html.Div(
        children=[
            html.H6(i18n.t("general.year")),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=to_dropdown_options(year_values),
                value=year_values,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
                id=ids.SELECT_ALL_YEARS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
