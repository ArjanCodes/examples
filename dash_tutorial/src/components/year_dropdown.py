import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.data.defaults import get_year_values
from src.data.manager import DataManager

from . import ids


def render(app: Dash, data_manager: DataManager) -> html.Div:
    @app.callback(
        Output(ids.YEAR_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_YEARS_BUTTON, "n_clicks"),
    )
    def select_all_years(_: int) -> list[str]:
        return data_manager.year_values

    return html.Div(
        children=[
            html.H6(i18n.t("general.year")),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=data_manager.year_options,
                value=data_manager.year_values,
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
