from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.config import SettingsSchema
from src.defaults import get_year_options, get_year_values
from src.schema import TransactionsSchema
from src.transactions import load_transaction_data

from . import ids


def render(app: Dash, settings: SettingsSchema) -> html.Div:
    transactions = load_transaction_data(settings.data.path)

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
        clicked = n_clicks <= previous_n_clicks
        new_years: list[str] = (
            years if clicked else list(set(transactions[TransactionsSchema.year]))
        )
        return sorted(new_years), n_clicks

    return html.Div(
        children=[
            html.H6(settings.components.year_dropdown.title),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=get_year_options(transactions),
                value=get_year_values(),
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=[settings.components.year_button.title],
                id=ids.YEAR_BUTTON,
                n_clicks=0,
            ),
        ]
    )
