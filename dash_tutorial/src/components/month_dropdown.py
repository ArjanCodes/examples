from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.config import SettingsSchema
from src.defaults import get_month_options, get_month_values
from src.schema import TransactionsSchema
from src.transactions import load_transaction_data


def render(app: Dash, settings: SettingsSchema) -> html.Div:
    transactions = load_transaction_data(settings.data.path)

    @app.callback(
        [
            Output(settings.components.month_dropdown.id, "value"),
            Output(settings.components.month_button_clicks.id, "data"),
        ],
        [
            Input(settings.components.year_dropdown.id, "value"),
            Input(settings.components.month_dropdown.id, "value"),
            Input(settings.components.month_button.id, "n_clicks"),
            Input(settings.components.month_button_clicks.id, "data"),
        ],
    )
    def select_all_months(
        years: list[int], months: list[str], n_clicks: int, previous_n_clicks: int
    ) -> tuple[list[str], int]:
        filtered_transactions = transactions.query(f"{TransactionsSchema.year} == {years}")
        clicked = n_clicks <= previous_n_clicks
        new_months: list[str] = (
            months if clicked else list(filtered_transactions[TransactionsSchema.month].unique())
        )
        return sorted(new_months), n_clicks

    return html.Div(
        children=[
            html.H6(settings.components.month_dropdown.title),
            dcc.Dropdown(
                id=settings.components.month_dropdown.id,
                options=get_month_options(transactions),
                value=get_month_values(),
                multi=True,
            ),
            html.Button(
                className=settings.components.month_button.class_name,
                children=[settings.components.month_button.title],
                id=settings.components.month_button.id,
                n_clicks=0,
            ),
        ]
    )
