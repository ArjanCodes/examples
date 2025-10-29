from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Depends

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

def get_service():
    return rate_service

@app.get("/convert")
@limiter.limit("5/minute")
def convert(..., service: ExchangeRateService = Depends(get_service)):
    ...