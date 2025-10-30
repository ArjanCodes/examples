from fastapi import FastAPI

app = FastAPI()

@app.get("/convert")
def convert(from_currency: str, to_currency: str, amount: float):
    rate = 1.1  # hardcoded
    return {"result": amount * rate}