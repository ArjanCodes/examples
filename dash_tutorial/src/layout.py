from dash import Dash, dcc, html

from src.components import (
    category_dropdown,
    month_dropdown,
    pie_chart,
    record_store,
    year_dropdown,
)
from src.config import SettingsSchema


def create_layout(app: Dash, settings: SettingsSchema) -> None:
    # initialize the record store
    record_store.initialize(app, settings)

    # create the pie chart
    pie_chart.initialize(app, settings)

    # create the layout
    app.layout = html.Div(
        className=settings.app.html_class_name,
        children=[
            html.H1(settings.app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    year_dropdown.render(app, settings),
                    month_dropdown.render(app, settings),
                    category_dropdown.render(app, settings),
                ],
            ),
            html.Div(id=settings.components.pie.id),
            dcc.Store(id=settings.components.records.id),
            dcc.Store(id=settings.components.year_button_clicks.id, data=0),
            dcc.Store(id=settings.components.month_button_clicks.id, data=0),
            dcc.Store(id=settings.components.category_button_clicks.id, data=0),
        ],
    )
