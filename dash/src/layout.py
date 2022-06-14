from dash import dcc, html

import src


def create_layout() -> html.Div:
    settings = src.config.load_settings()
    return html.Div(
        className=settings.app.html_class_name,
        children=[
            html.H1(settings.app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    src.components.year_dropdown.render(),
                    src.components.month_dropdown.render(),
                    src.components.category_dropdown.render(),
                ],
            ),
            html.Div(id=settings.components.pie.id),
            dcc.Store(id=settings.components.records.id),
            dcc.Store(id=settings.components.year_button_clicks.id, data=0),
            dcc.Store(id=settings.components.month_button_clicks.id, data=0),
            dcc.Store(id=settings.components.category_button_clicks.id, data=0),
        ],
    )
