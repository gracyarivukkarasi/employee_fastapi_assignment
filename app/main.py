from fastapi import Depends, FastAPI, HTTPException, Path, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.schemas import (
    EmployeeCreate,
    EmployeeListResponse,
    EmployeeResponse,
    EmployeeUpdate,
    WorkMode,
)
from app.services import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
)

app = FastAPI(title="Employee Management API")
Base.metadata.create_all(bind=engine)

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


@app.get("/employees", response_model=EmployeeListResponse)
def get_employees(
    search: str | None = Query(
        default=None,
        description="Search employees by name"
    ),
    department: str | None = Query(
        default=None,
        description="Filter employees by department"
    ),
    work_mode: WorkMode | None = Query(
        default=None,
        description="Filter employees by work mode"
    ),
    is_active: bool | None = Query(
        default=None,
        description="Filter employees by active status"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of records to return"
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of records to skip"
    ),
    db: Session = Depends(get_db),
):
    return get_all_employees(
        db=db,
        search=search,
        department=department,
        work_mode=work_mode.value if work_mode else None,
        is_active=is_active,
        limit=limit,
        offset=offset,
    )
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
    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    try:
        deleted_employee = delete_employee(
            db,
            employee_id
        )

        return {
            "message": "Employee deleted successfully"
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete employee"
        )