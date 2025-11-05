import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Hardcoded exchange rates (not production-ready!)
RATES = {
    ("USD", "EUR"): 0.91,
    ("EUR", "USD"): 1.10,
    ("USD", "JPY"): 150.0,
}


@app.get("/convert")
def convert(from_currency: str, to_currency: str, amount: float):
    key = (from_currency.upper(), to_currency.upper())
    rate = RATES.get(key)

    if rate is None:
        raise HTTPException(status_code=400, detail="Exchange rate not available")

    return {"result": amount * rate}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
