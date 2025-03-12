from fastapi import FastAPI

app = FastAPI()

FEATURE_GOODBYES = True
FEATURE_HELLO_NAME = True


if FEATURE_HELLO_NAME:

    @app.get("/")
    def hello(name: str = "World"):
        return f"Hello, {name}!"

else:

    @app.get("/")
    def hello():
        return "Hello, World!"


if FEATURE_GOODBYES:

    @app.get("/goodbye")
    def goodbye():
        return "Goodbye, World!"
