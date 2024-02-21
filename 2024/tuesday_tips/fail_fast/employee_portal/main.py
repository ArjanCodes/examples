from fastapi import Depends, FastAPI, HTTPException
from decimal import Decimal
from typing import Any
from employee_portal.database.database import SQLiteConnector
from employee_portal.employees import create, delete, index, show, update
from employee_portal.payment import (
    CreditCardPayment,
    PaymentProcessor,
    RedeemBuddyPayment,
)
from employee_portal.position import Position

app = FastAPI()


async def setup_db_connection() -> SQLiteConnector:
    return SQLiteConnector()


async def setup_payment_processor() -> PaymentProcessor:
    return PaymentProcessor()


@app.post("/employees/", response_model=None)
def create_employee(
    name: str,
    position: Position,
    salary: Decimal,
    connector: SQLiteConnector = Depends(setup_db_connection),
):
    create(connector, name, position, salary)
    return {"message": "Record inserted successfully"}


@app.get("/employees/", response_model=list[tuple[Any, ...]])
def read_employees(connector: SQLiteConnector = Depends(setup_db_connection)):
    return index(connector)


@app.get("/employees/{employee_id}", response_model=tuple[Any, ...])
def read_employee(
    employee_id: int, connector: SQLiteConnector = Depends(setup_db_connection)
):
    employee = show(connector, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.put("/employees/{employee_id}", response_model=None)
def update_employee(
    employee_id: int,
    name: str,
    position: Position,
    salary: Decimal,
    connector: SQLiteConnector = Depends(setup_db_connection),
):
    existing_employee = show(connector, employee_id)
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    update(connector, employee_id, name, position, salary)
    return {"message": f"Employee with ID {employee_id} updated successfully"}


@app.delete("/employees/{employee_id}", response_model=None)
def delete_employee(
    employee_id: int, connector: SQLiteConnector = Depends(setup_db_connection)
):
    existing_employee = show(connector, employee_id)
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    delete(connector, employee_id)
    return {"message": f"Employee with ID {employee_id} deleted successfully"}


@app.post("/pay_salary/{employee_id}")
def pay_salary(
    employee_id: int,
    payment_method: str,
    payment_processor: PaymentProcessor = Depends(setup_payment_processor),
    connector: SQLiteConnector = Depends(setup_db_connection),
):
    employee_info = show(connector, employee_id)

    amount = employee_info[-1]

    if not employee_info:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Create a payment processor based on the selected payment method
    if payment_method == "credit_card":
        credit_card_payment = CreditCardPayment()
        payment_processor.set_payment_strategy(credit_card_payment)
    elif payment_method == "redeem_buddy":
        redeem_buddy_payment = RedeemBuddyPayment()
        payment_processor.set_payment_strategy(redeem_buddy_payment)
    else:
        raise HTTPException(status_code=400, detail="Invalid payment method")

    # Process the salary payment
    payment_processor.process_payment(amount)

    return {"message": f"Salary paid {amount} successfully to employee {employee_id}"}
