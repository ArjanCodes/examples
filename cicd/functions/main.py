from flask.wrappers import Request, Response
from routes import app


def channel_api(request: Request) -> Response:
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
