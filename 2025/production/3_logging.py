import logging
import sentry_sdk
from fastapi import HTTPException, Request

sentry_sdk.init(dsn=settings.sentry_dsn)
logging.basicConfig(level=settings.log_level)

@app.get("/convert")
def convert(..., request: Request):
    try:
        rate = 1.1  # or from a service
        result = float(amount * rate)
        logging.info(f"Converted {amount} {from_currency} → {to_currency}")
        return {"result": result}
    except Exception as e:
        logging.error(f"Conversion failed: {e}")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Internal error")

@app.get("/health")
def health():
    return {"status": "ok"}