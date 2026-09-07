from fastapi import FastAPI, HTTPException, Path
from app.schemas import Employee, EmployeeCreate, EmployeeUpdate
from app.services import (
    create_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    delete_employee
)

app = FastAPI(title="Employee Management API")

@app.get("/health")
def health_check():
    return {"status": "Application is running"}


@app.post("/employees", response_model=Employee, status_code=201)
def create_employee_api(employee: EmployeeCreate):
    new_employee = create_employee(employee)

    if new_employee is None:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return new_employee
@app.get("/employees", response_model=list[Employee])
def get_employees():
    return get_all_employees()
@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int = Path(..., gt=0)):
    employee = get_employee_by_id(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee

@app.put("/employees/{employee_id}", response_model=Employee)
def update_employee_api(
    employee_data: EmployeeUpdate,
    employee_id: int = Path(..., gt=0)
):
    employee = get_employee_by_id(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    updated_employee = update_employee(employee_id, employee_data)

    if updated_employee is None:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return updated_employee

@app.delete("/employees/{employee_id}")
def delete_employee_api(employee_id: int = Path(..., gt=0)):
    employee = delete_employee(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {"message": "Employee deleted successfully"}
