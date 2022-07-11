from dash import Dash, dcc, html
from src.components import (
    bar_chart,
    category_dropdown,
    month_dropdown,
    pie_chart,
    record_store,
    year_dropdown,
)

from ..data.source import DataSource
from . import ids


def create_layout(app: Dash, data: DataSource) -> html.Div:
    # initialize the record store
    record_store.initialize(app, data)

    # create the layout
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    year_dropdown.render(app, data),
                    month_dropdown.render(app, data),
                    category_dropdown.render(app, data),
                ],
            ),
            bar_chart.render(app),
            pie_chart.render(app, data),
            dcc.Store(id=ids.RECORDS),
        ],
    )
