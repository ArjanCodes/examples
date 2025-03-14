from fastapi import FastAPI

app = FastAPI()

FEATURE_GOODBYE = True
FEATURE_FORMAL = True


if FEATURE_FORMAL:

    @app.get("/")
    def hello_formal(name: str = "World", formal: bool = False):
        if formal:
            return f"Good day to you, {name}."
        return f"Hello, {name}!"

else:

    @app.get("/")
    def hello(name: str = "World"):
        return f"Hello, {name}!"


if FEATURE_GOODBYE:

    @app.get("/goodbye")
    def goodbye(name: str = "World"):
        return f"Goodbye, {name}!"
