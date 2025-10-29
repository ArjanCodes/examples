import logging
from fastapi import HTTPException, Request
import sentry_sdk

logging.basicConfig(level=logging.INFO)
sentry_sdk.init(dsn="your-sentry-dsn")  # from config

@app.get("/convert")
def convert(..., request: Request):
    try:
        rate = 1.1
        result = float(amount * rate)
        logging.info(f"Converted {amount} {from_currency} → {to_currency}")
        return {"result": result}
    except Exception as e:
        logging.error(f"Conversion failed: {e}")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Internal error")