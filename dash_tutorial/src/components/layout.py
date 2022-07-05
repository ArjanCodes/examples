from dash import Dash, dcc, html
from src.components import (
    bar_chart,
    category_dropdown,
    month_dropdown,
    pie_chart,
    record_store,
    year_dropdown,
)
from src.data.manager import DataManager

from . import ids


def create_layout(app: Dash, data_manager: DataManager) -> html.Div:
    # initialize the record store
    record_store.initialize(app, data_manager)

    # create the layout
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    year_dropdown.render(app, data_manager),
                    month_dropdown.render(app, data_manager),
                    category_dropdown.render(app, data_manager),
                ],
            ),
            bar_chart.render(app),
            pie_chart.render(app),
            dcc.Store(id=ids.RECORDS),
        ],
    )
