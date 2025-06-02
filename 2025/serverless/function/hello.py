import flask
import functions_framework


@functions_framework.http
def hello_handler(request: flask.Request) -> flask.Response:
    return flask.Response("Hello, World!", status=200)
