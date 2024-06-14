from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "healthy!"}


@app.api_route("/", methods=["STATEMENT"])
def statement() -> dict[str, str]:
    return {"STATEMENT": "I love the name Evelina because it contains liv"}
