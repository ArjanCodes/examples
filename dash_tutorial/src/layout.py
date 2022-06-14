from dash import dcc, html

from src.components import category_dropdown, month_dropdown, year_dropdown
from src.config import SETTINGS


def create_layout() -> html.Div:
    return html.Div(
        className=SETTINGS.app.html_class_name,
        children=[
            html.H1(SETTINGS.app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    year_dropdown.render(),
                    month_dropdown.render(),
                    category_dropdown.render(),
                ],
            ),
            html.Div(id=SETTINGS.components.pie.id),
            dcc.Store(id=SETTINGS.components.records.id),
            dcc.Store(id=SETTINGS.components.year_button_clicks.id, data=0),
            dcc.Store(id=SETTINGS.components.month_button_clicks.id, data=0),
            dcc.Store(id=SETTINGS.components.category_button_clicks.id, data=0),
        ],
    )
