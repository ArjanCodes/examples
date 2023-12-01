import string
from dash import Dash, html

from src.data.reader import load_json
from src.formatter import title_case


from . import line_chart


def create_layout(app: Dash) -> html.Div:
    data = load_json("dashboard/data/output.json")

    string.capwords
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            line_chart.render(app, data),
            html.Div(
                className="cardbox",
                children = [
                    html.Li(
                        id=key,
                        className="card",
                        children=[
                            html.H3(id=key, children=[title_case(key)]),
                            html.Code(data[key].pattern),
                        ],
                    )
                    for key in data
                ]
            ),
        ],
    )
