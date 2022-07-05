import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from pandas import DataFrame
from src.data import DataSchema
from src.defaults import get_month_options, get_month_values

from . import ids


def render(app: Dash, data: DataFrame) -> html.Div:
    @app.callback(
        Output(ids.MONTH_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_MONTHS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_months(years: list[int], _: int) -> list[str]:
        filtered_transactions = data.query(f"{DataSchema.YEAR.value} == {years}")
        return sorted(get_month_values(filtered_transactions))

    return html.Div(
        children=[
            html.H6(i18n.t("general.month")),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=get_month_options(data),
                value=get_month_values(data),
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
