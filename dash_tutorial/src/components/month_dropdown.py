import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.manager import DataManager
from . import ids


def render(app: Dash, data_manager: DataManager) -> html.Div:
    @app.callback(
        Output(ids.MONTH_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_MONTHS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_months(years: list[str], _: int) -> list[str]:
        return data_manager.month_values(years)

    return html.Div(
        children=[
            html.H6(i18n.t("general.month")),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=data_manager.month_options,
                value=data_manager.month_values(),
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
