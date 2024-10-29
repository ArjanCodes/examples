from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.models import Payment
from src.payment_processor import process_payment

payment_route = APIRouter()


@payment_route.post("/payment")
async def make_payment(params: Payment) -> JSONResponse:
    if params.customer_id is None:
        return HTTPException(
            status_code=400, content={"message": "Customer ID is required"}
        )
    

    payment_amount = process_payment(amount=params.amount, discount_percent=21)


    return {"message": f"Payment has been made: ${payment_amount:.2f}"}
