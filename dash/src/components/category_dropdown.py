import src
from dash import dcc, html


def render() -> html.Div:
    settings = src.config.load_settings()
    transactions = src.transactions.load_transaction_data()
    return html.Div(
        children=[
            html.H6(settings.components.category_dropdown.title),
            dcc.Dropdown(
                id=settings.components.category_dropdown.id,
                options=src.defaults.get_category_options(transactions),
                value=src.defaults.get_category_values(transactions),
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
