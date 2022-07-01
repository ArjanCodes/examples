import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from pandas import DataFrame
from src.defaults import get_category_options, get_category_values
from src.schema import TransactionsSchema

from . import ids


def render(app: Dash, transactions: DataFrame) -> html.Div:
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
            html.H6(i18n.t("general.category")),
            dcc.Dropdown(
                id=ids.CATEGORY_DROPDOWN,
                options=get_category_options(transactions),
                value=get_category_values(transactions),
                multi=True,
                placeholder=i18n.t("general.select"),
            ),
            html.Button(
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
                id=ids.CATEGORY_BUTTON,
                n_clicks=0,
            ),
        ],
    )
