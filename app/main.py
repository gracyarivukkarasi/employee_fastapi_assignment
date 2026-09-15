from fastapi import Depends, FastAPI, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
)

app = FastAPI(title="Employee Management API")


@app.get("/health")
def health_check():
    return {"status": "Application is running"}


@app.post("/employees", response_model=EmployeeResponse, status_code=201)
def create_employee_api(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    try:
        new_employee = create_employee(db, employee)

        if new_employee is None:
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

        return new_employee

    except HTTPException:
        raise

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create employee"
        )


@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return get_all_employees(db)


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee_api(
    employee_data: EmployeeUpdate,
    employee_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    try:
        updated_employee = update_employee(
            db,
            employee_id,
            employee_data
        )

        if updated_employee is None:
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

        return updated_employee

    except HTTPException:
        raise

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to update employee"
        )


@app.delete("/employees/{employee_id}")
def delete_employee_api(
    employee_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    employee = delete_employee(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {"message": "Employee deleted successfully"}