from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.config import SettingsSchema
from src.defaults import get_category_options, get_category_values
from src.schema import MonthColumnSchema, RawTransactionsSchema, YearColumnSchema
from src.transactions import load_transaction_data


def render(app: Dash, settings: SettingsSchema) -> html.Div:
    transactions = load_transaction_data(settings.data.path)

    @app.callback(
        Output(settings.components.category_dropdown.id, "value"),
        [
            Input(settings.components.year_dropdown.id, "value"),
            Input(settings.components.month_dropdown.id, "value"),
            Input(settings.components.category_button.id, "n_clicks"),
        ],
    )
    def select_all_categories(
        year: list[int], month: list[int], _: list[int]
    ) -> list[str]:
        categories: list[str] = list(
            transactions.query(
                f"({YearColumnSchema.year} == {year}) "
                f"& ({MonthColumnSchema.month} == {month})"
            )
            .loc[:, RawTransactionsSchema.category]
            .unique()
        )
        return sorted(categories)

    return html.Div(
        children=[
            html.H6(settings.components.category_dropdown.title),
            dcc.Dropdown(
                id=settings.components.category_dropdown.id,
                options=get_category_options(transactions),
                value=get_category_values(transactions),
                multi=True,
            ),
            html.Button(
                className=settings.components.category_button.class_name,
                children=[settings.components.category_button.title],
                id=settings.components.category_button.id,
                n_clicks=0,
            ),
        ],
    )
