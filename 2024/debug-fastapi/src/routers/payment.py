from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.models import Payment

payment_route = APIRouter()


@payment_route.post("/payment")
async def make_payment(params: Payment) -> JSONResponse:
    if params.customer_id is None:
        return HTTPException(
            status_code=400, content={"message": "Customer ID is required"}
        )

    return {"message": "Payment has been made"}
