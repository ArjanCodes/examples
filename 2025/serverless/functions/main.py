import flask
import functions_framework


@functions_framework.http
def hello(request: flask.Request) -> flask.Response:
    return flask.Response("Hello, World!", status=200)
