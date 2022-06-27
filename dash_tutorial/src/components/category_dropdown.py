from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.config import SettingsSchema
from src.defaults import get_category_options, get_category_values
from src.schema import TransactionsSchema
from src.transactions import load_transaction_data

from . import ids


def render(app: Dash, settings: SettingsSchema) -> html.Div:
    transactions = load_transaction_data(settings.data.path)

    @app.callback(
        Output(ids.CATEGORY_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_BUTTON, "n_clicks"),
        ],
    )
    def select_all_categories(
        year: list[int], month: list[int], _: list[int]
    ) -> list[str]:
        categories: list[str] = list(
            transactions.query(
                f"({TransactionsSchema.year} == {year}) "
                f"& ({TransactionsSchema.month} == {month})"
            )
            .loc[:, TransactionsSchema.category]
            .unique()
        )
        return sorted(categories)

    return html.Div(
        children=[
            html.H6(settings.components.category_dropdown.title),
            dcc.Dropdown(
                id=ids.CATEGORY_DROPDOWN,
                options=get_category_options(transactions),
                value=get_category_values(transactions),
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=[settings.components.category_button.title],
                id=ids.CATEGORY_BUTTON,
                n_clicks=0,
            ),
        ],
    )
