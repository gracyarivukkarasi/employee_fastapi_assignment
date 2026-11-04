import os
from contextlib import asynccontextmanager

import httpx
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.database import Base, engine, get_db


load_dotenv()

EMPLOYEE_SERVICE_URL = os.getenv(
    "EMPLOYEE_SERVICE_URL",
    "http://localhost:8001",
).rstrip("/")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Work Item Service",
    description="Work Item microservice for Task 6",
    version="1.0.0",
    lifespan=lifespan,
)


def verify_employee(employee_id: int) -> None:
    url = f"{EMPLOYEE_SERVICE_URL}/employees/{employee_id}"

    try:
        response = httpx.get(url, timeout=5.0)

        if response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found",
            )

        response.raise_for_status()

    except HTTPException:
        raise

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Employee Service returned an unexpected error",
        ) from exc

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Employee Service is unavailable or timed out",
        ) from exc


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Work Item Service",
    }


@app.post(
    "/work-items",
    response_model=schemas.WorkItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_work_item(
    work_item: schemas.WorkItemCreate,
    db: Session = Depends(get_db),
):
    # New work items must start with TODO.
    # Invalid or null status values are rejected by Pydantic with 422.
    if work_item.status != schemas.WorkItemStatus.TODO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New work items must have status TODO",
        )

    # Verify the employee before saving anything.
    verify_employee(work_item.employee_id)

    return services.create_work_item(db, work_item)


@app.get(
    "/work-items",
    response_model=list[schemas.WorkItemResponse],
)
def get_work_items(db: Session = Depends(get_db)):
    return services.get_all_work_items(db)


@app.get(
    "/work-items/{work_item_id}",
    response_model=schemas.WorkItemResponse,
)
def get_work_item(
    work_item_id: int,
    db: Session = Depends(get_db),
):
    work_item = services.get_work_item_by_id(db, work_item_id)

    if work_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work item not found",
        )

    return work_item