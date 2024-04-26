from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def health_check() -> str:
    return "Service is healthy!"
