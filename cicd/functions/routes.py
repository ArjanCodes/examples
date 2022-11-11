from flask import Flask
from flask.wrappers import Response
from operations import get_channel

# Define an internal Flask app
app = Flask("internal")

# Define the internal paths, idiomatic Flask definition
@app.route("/channels/<string:channel_id>", methods=["GET", "POST"])
def channel(channel_id: str):
    return get_channel(channel_id)


@app.route("/", methods=["GET"])
def index():
    return Response("Channel API is running.", status=200)
