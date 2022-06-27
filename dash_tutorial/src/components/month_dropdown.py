from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.config import SettingsSchema
from src.defaults import get_month_options, get_month_values
from src.schema import TransactionsSchema
from src.transactions import load_transaction_data

from . import ids


def render(app: Dash, settings: SettingsSchema) -> html.Div:
    transactions = load_transaction_data(settings.data.path)

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
        filtered_transactions = transactions.query(
            f"{TransactionsSchema.year} == {years}"
        )
        clicked = n_clicks <= previous_n_clicks
        new_months: list[str] = (
            months
            if clicked
            else list(set(filtered_transactions[TransactionsSchema.month]))
        )
        return sorted(new_months), n_clicks

    return html.Div(
        children=[
            html.H6(settings.components.month_dropdown.title),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=get_month_options(transactions),
                value=get_month_values(),
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=[settings.components.month_button.title],
                id=ids.MONTH_BUTTON,
                n_clicks=0,
            ),
        ]
    )
