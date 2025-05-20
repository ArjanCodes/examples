import json
from typing import Any

import flask
import functions_framework

# Define an internal Flask app
app = flask.Flask("internal")


channels: dict[str, Any] = {}

with open("channels.json", encoding="utf8") as file:
    channels_raw = json.load(file)
    for channel_raw in channels_raw:
        channels[channel_raw["id"]] = channel_raw


# Define the internal path, idiomatic Flask definition
@app.route("/channels/<string:channel_id>", methods=["GET", "POST"])
def name(channel_id: str):
    if channel_id not in channels:
        return flask.Response("Channel not found", status=404)
    return flask.Response(json.dumps(channels[channel_id]), status=200)


@functions_framework.http
def channels_handler(request: flask.Request) -> flask.Response:
    # Create a new app context for the internal app
    ctx = app.test_request_context(
        path=request.full_path,
        method=request.method,
    )
    ctx.request = request
    ctx.push()
    response = app.full_dispatch_request()
    ctx.pop()
    return response
