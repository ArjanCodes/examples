# skypulse

API for getting historical weatcher events

## Development Requirements

- Python3.11.0
- Pip
- Poetry (Python Package Manager)

## Installation

```sh
python -m venv venv
source venv/bin/activate
make install
```

## Runnning Localhost

`make run`

## Deploy app

`make deploy`

## Running Tests

`make test`

## Access Swagger Documentation

> <http://localhost:8080/docs>

## Access Redocs Documentation

> <http://localhost:8080/redoc>

## Project structure
    app
    ├── api                 - API related functionaltiy.
    │   └── routes          - Routes for API.
    ├── core                - application configuration, startup events, logging.
    ├── models              - pydantic models for this application.
    ├── schemas             - TODO
    ├── services            - logic that is not just crud related.
    └── main.py             - FastAPI application creation and configuration.
    └── tests            - pytest

## Source
Based on and altered from <https://github.com/arthurhenrique/cookiecutter-fastapi/graphs/contributors>
