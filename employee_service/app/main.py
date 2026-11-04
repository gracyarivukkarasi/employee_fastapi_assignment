from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.database import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Employee Service",
    description="Employee microservice for Task 6",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Employee Service",
    }


@app.post(
    "/employees",
    response_model=schemas.EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
):
    try:
        existing_employee = (
            db.query(models.Employee)
            .filter(
                models.Employee.email == str(employee.email)
            )
            .first()
        )

        if existing_employee:
            raise HTTPException(
                status_code=400,
                detail="Employee email already exists",
            )

        return services.create_employee(db, employee)

    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Employee email already exists",
        ) from exc


@app.get(
    "/employees",
    response_model=list[schemas.EmployeeResponse],
)
def get_employees(db: Session = Depends(get_db)):
    return services.get_all_employees(db)


@app.get(
    "/employees/{employee_id}",
    response_model=schemas.EmployeeResponse,
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):
    employee = services.get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return employee