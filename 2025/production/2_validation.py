from decimal import Decimal

import uvicorn
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

# Hardcoded exchange rates as Decimals
RATES = {
    ("USD", "EUR"): Decimal("0.91"),
    ("EUR", "USD"): Decimal("1.10"),
    ("USD", "JPY"): Decimal("150.0"),
}


@app.get("/convert")
def convert(
    from_currency: str = Query(..., min_length=3, max_length=3),
    to_currency: str = Query(..., min_length=3, max_length=3),
    amount: Decimal = Query(..., gt=0),
):
    key = (from_currency.upper(), to_currency.upper())
    rate = RATES.get(key)

    if rate is None:
        raise HTTPException(status_code=400, detail="Exchange rate not available")

    result = amount * rate  # both Decimal
    return {"rate": float(rate), "result": float(result)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
