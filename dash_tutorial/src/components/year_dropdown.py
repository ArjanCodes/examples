from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.config import SettingsSchema
from src.defaults import get_year_options, get_year_values
from src.schema import TransactionsSchema
from src.transactions import load_transaction_data


def render(app: Dash, settings: SettingsSchema) -> html.Div:
    transactions = load_transaction_data(settings.data.path)

    @app.callback(
        [
            Output(settings.components.year_dropdown.id, "value"),
            Output(settings.components.year_button_clicks.id, "data"),
        ],
        [
            Input(settings.components.year_dropdown.id, "value"),
            Input(settings.components.year_button.id, "n_clicks"),
            Input(settings.components.year_button_clicks.id, "data"),
        ],
    )
    def select_all_years(
        years: list[str], n_clicks: int, previous_n_clicks: int
    ) -> tuple[list[str], int]:
        clicked = n_clicks <= previous_n_clicks
        new_years: list[str] = (
            years if clicked else list(transactions[TransactionsSchema.year].unique())
        )
        return sorted(new_years), n_clicks

    return html.Div(
        children=[
            html.H6(settings.components.year_dropdown.title),
            dcc.Dropdown(
                id=settings.components.year_dropdown.id,
                options=get_year_options(transactions),
                value=get_year_values(),
                multi=True,
            ),
            html.Button(
                className=settings.components.year_button.class_name,
                children=[settings.components.year_button.title],
                id=settings.components.year_button.id,
                n_clicks=0,
            ),
        ]
    )
