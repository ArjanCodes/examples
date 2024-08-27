from typing import Any
from requests import Response, request


# The order matters
# Args are positional arguments stored in a tuple are denoted by *
# Kwargs are keyword arguments stored in a dictionary are denoted by **
# The order should be required arguments, *args, **kwargs
# Args should be used when the number of arguments is not fixed
# Kwargs should be used when the number of keyword arguments is not fixed

DEFAULT_HEADERS = {"Content-Type": "application/json"}


# An example to add default functionaltiy to the request function
# And still having the ability to pass custom headers
# Making it more flexible and easier to use
def api_request(
    method: str, url: str, *args: Any, **kwargs: dict[str, Any]
) -> Response:
    headers = kwargs.pop("headers", {})
    headers.update(DEFAULT_HEADERS)
    return request(method, url, *args, headers=headers, **kwargs)


# Args can be used to pass a variable number of arguments
# As long as they are of the same type (In this case, float)
# And the return type is the same as the arguments
# The name of the args can be anything, but typically it would be args
# As long as you use the * operator
def summarize(*floats: float) -> float:
    return sum(floats)


# Same goes for kwargs, typically it would be kwargs, but in reality you can name these anything
# As long as you use the ** operator
def load_config(
    defaults: dict[str, Any], **overrides: dict[str, Any]
) -> dict[str, Any]:
    config = defaults.copy()
    config.update(overrides)
    return config
