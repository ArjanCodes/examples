from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import condecimal
from sqlalchemy.orm import Session
from .database import get_db
from .services import ExchangeRateService
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/convert")
@limiter.limit("5/minute")
def convert(
    request: Request,
    from_currency: str = Query(..., min_length=3, max_length=3),
    to_currency: str = Query(..., min_length=3, max_length=3),
    amount: condecimal(gt=0) = Query(...),
    db: Session = Depends(get_db),
):
    try:
        service = ExchangeRateService(db)
        return service.convert(from_currency, to_currency, float(amount))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    return {"status": "ok"}