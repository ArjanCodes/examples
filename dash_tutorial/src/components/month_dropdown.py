import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from pandas import DataFrame
from src.defaults import get_month_options, get_month_values
from src.schema import DataSchema

from . import ids


def render(app: Dash, data: DataFrame) -> html.Div:
    @app.callback(
        [
            Output(ids.MONTH_DROPDOWN, "value"),
            Output(ids.MONTH_BUTTON_CLICKS, "data"),
        ],
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.MONTH_BUTTON, "n_clicks"),
            Input(ids.MONTH_BUTTON_CLICKS, "data"),
        ],
    )
    def select_all_months(
        years: list[int], months: list[str], n_clicks: int, previous_n_clicks: int
    ) -> tuple[list[str], int]:
        filtered_transactions = data.query(f"{DataSchema.YEAR.value} == {years}")
        clicked = n_clicks <= previous_n_clicks
        new_months: list[str] = (
            months
            if clicked
            else list(set(filtered_transactions[DataSchema.MONTH.value]))
        )
        return sorted(new_months), n_clicks

    return html.Div(
        children=[
            html.H6(i18n.t("general.month")),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=get_month_options(data),
                value=get_month_values(),
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
                id=ids.MONTH_BUTTON,
                n_clicks=0,
            ),
        ]
    )
