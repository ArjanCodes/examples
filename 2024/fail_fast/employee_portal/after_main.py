from fastapi import FastAPI, HTTPException
from decimal import Decimal
from typing import Any, List, Tuple
from employee_portal.database.database import SQLiteConnector
from employee_portal.employees import create, delete, index, show, update
from employee_portal.payment import (
    CreditCardPayment,
    PaymentProcessor,
    RedeemBuddyPayment,
)
from employee_portal.position import Position

app = FastAPI()

connector = SQLiteConnector()

credit_card_payment = CreditCardPayment()
redeem_buddy_payment = RedeemBuddyPayment()

payment_processor = PaymentProcessor(redeem_buddy_payment)


@app.post("/employees/", response_model=None)
def create_employee(name: str, position: Position, salary: Decimal):
    if not isinstance(salary, float):
        raise HTTPException(status_code=400, detail="Salart type or value is incorrect. Use decimal")
    
    if salary < 0:
        raise HTTPException(status_code=400, detail="Salart value is incorrect. Give an positive decimal value")

    create(connector, name, position, salary)
    return {"message": "Record inserted successfully"}


@app.get("/employees/", response_model=List[Tuple[Any, ...]])
def read_employees():
    return index(connector)


@app.get("/employees/{employee_id}", response_model=Tuple[Any, ...])
def read_employee(employee_id: int):
    employee = show(connector, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.put("/employees/{employee_id}", response_model=None)
def update_employee(employee_id: int, name: str, position: Position, salary: Decimal):
    existing_employee = show(connector, employee_id)
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if not isinstance(salary, float):
        raise HTTPException(status_code=400, detail="Salart type or value is incorrect. Use decimal")
    
    if salary < 0:
        raise HTTPException(status_code=400, detail="Salart value is incorrect. Give an positive decimal value")

    update(connector, employee_id, name, position, salary)
    return {"message": f"Employee with ID {employee_id} updated successfully"}


@app.delete("/employees/{employee_id}", response_model=None)
def delete_employee(employee_id: int):
    existing_employee = show(connector, employee_id)
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    delete(connector, employee_id)
    return {"message": f"Employee with ID {employee_id} deleted successfully"}


@app.post("/pay_salary/{employee_id}")
def pay_salary(employee_id: int, payment_method: str):
    employee_info = show(connector, employee_id)

    amount = employee_info[-1]

    if not employee_info:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Create a payment processor based on the selected payment method
    if payment_method == "credit_card":
        payment_processor.set_payment_strategy(credit_card_payment)
    elif payment_method == "redeem_buddy":
        payment_processor.set_payment_strategy(redeem_buddy_payment)
    else:
        raise HTTPException(status_code=400, detail="Invalid payment method")

    # Process the salary payment
    payment_processor.process_payment(amount)

    return {"message": f"Salary paid {amount} successfully to employee {employee_id}"}
