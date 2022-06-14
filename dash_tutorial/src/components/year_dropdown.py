import src
from dash import dcc, html


def render() -> html.Div:
    settings = src.config.load_settings()
    return html.Div(
        children=[
            html.H6(settings.components.year_dropdown.title),
            dcc.Dropdown(
                id=settings.components.year_dropdown.id,
                options=src.defaults.get_year_options(
                    src.transactions.load_transaction_data()
                ),
                value=src.defaults.get_year_values(),
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
