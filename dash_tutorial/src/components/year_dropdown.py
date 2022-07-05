from typing import Protocol

import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from . import ids


class DataSource(Protocol):
    @property
    def year_options(self) -> list[dict[str, str]]:
        """Available options for the year dropdown"""

    def year_values(self) -> list[str]:
        """Available year values."""


def render(app: Dash, data_source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.YEAR_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_YEARS_BUTTON, "n_clicks"),
    )
    def select_all_years(_: int) -> list[str]:
        return data_source.year_values()

    return html.Div(
        children=[
            html.H6(i18n.t("general.year")),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=data_source.year_options,
                value=data_source.year_values(),
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
