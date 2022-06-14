import src
from dash import dcc, html


def render() -> html.Div:
    settings = src.config.load_settings()
    return html.Div(
        children=[
            html.H6(settings.components.month_dropdown.title),
            dcc.Dropdown(
                id=settings.components.month_dropdown.id,
                options=src.defaults.get_month_options(src.transactions.load_transaction_data()),
                value=src.defaults.get_month_values(),
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
