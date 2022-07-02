import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from pandas import DataFrame
from src.defaults import get_year_options, get_year_values
from src.schema import DataSchema

from . import ids


def render(app: Dash, data: DataFrame) -> html.Div:
    @app.callback(
        [
            Output(ids.YEAR_DROPDOWN, "value"),
            Output(ids.YEAR_BUTTON_CLICKS, "data"),
        ],
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.YEAR_BUTTON, "n_clicks"),
            Input(ids.YEAR_BUTTON_CLICKS, "data"),
        ],
    )
    def select_all_years(
        years: list[str], n_clicks: int, previous_n_clicks: int
    ) -> tuple[list[str], int]:
        clicked = (n_clicks <= previous_n_clicks) or (n_clicks == 0)
        new_years: list[str] = (
            years if clicked else list(set(data[DataSchema.YEAR.value]))
        )
        return sorted(new_years), n_clicks

    return html.Div(
        children=[
            html.H6(i18n.t("general.year")),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=get_year_options(data),
                value=get_year_values(),
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
                id=ids.YEAR_BUTTON,
                n_clicks=0,
            ),
        ]
    )
