from pydantic import condecimal
from fastapi import Query

@app.get("/convert")
def convert(
    from_currency: str = Query(..., min_length=3, max_length=3),
    to_currency: str = Query(..., min_length=3, max_length=3),
    amount: condecimal(gt=0) = Query(...)
):
    rate = 1.1
    return {"result": float(amount * rate)}