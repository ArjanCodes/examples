import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from pandas import DataFrame
from src.defaults import get_year_options, get_year_values

from . import ids


def render(app: Dash, data: DataFrame) -> html.Div:
    @app.callback(
        Output(ids.YEAR_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_YEARS_BUTTON, "n_clicks"),
    )
    def select_all_years(_: int) -> list[str]:
        return sorted(get_year_values(data))

    return html.Div(
        children=[
            html.H6(i18n.t("general.year")),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=get_year_options(data),
                value=get_year_values(data),
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
