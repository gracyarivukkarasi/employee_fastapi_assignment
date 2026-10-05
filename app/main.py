from fastapi import Depends, FastAPI, HTTPException, Path, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, get_db
from app.schemas import (
    EmployeeCreate,
    EmployeeListResponse,
    EmployeeResponse,
    EmployeeUpdate,
    WorkMode,
    WorkItemCreate,
    WorkItemListResponse,
    WorkItemResponse,
    WorkItemStatus,
    WorkItemPriority,
    WorkItemUpdate,
)
from app.services import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    create_work_item,
    delete_work_item,
    get_all_work_items,
    get_work_item_by_id,
    update_work_item,
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


@app.delete("/employees/{employee_id}", status_code=204)
def delete_employee_api(
    employee_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    deleted_employee = delete_employee(db, employee_id)

    if deleted_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if deleted_employee == "has_work_items":
        raise HTTPException(
            status_code=409,
            detail="Cannot delete employee because they have assigned work items. Reassign or delete the work items first."
        )

    return None

@app.post(
    "/work-items",
    response_model=WorkItemResponse,
    status_code=201
)
def create_work_item_api(
    work_item: WorkItemCreate,
    db: Session = Depends(get_db)
):
    new_work_item = create_work_item(
        db,
        work_item
    )
    if new_work_item == "database_error":
        raise HTTPException(
            status_code=500,
            detail="Failed to create work item due to a database error"
        )

    if new_work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return new_work_item

@app.get(
    "/work-items",
    response_model=WorkItemListResponse
)
def get_work_items(
    search: str | None = Query(
        default=None,
        description="Search work items by title"
    ),
    employee_id: int | None = Query(
        default=None,
        gt=0,
        description="Filter by employee ID"
    ),
    status: WorkItemStatus | None = Query(
        default=None,
        description="Filter by status"
    ),
    priority: WorkItemPriority | None = Query(
        default=None,
        description="Filter by priority"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),
    offset: int = Query(
        default=0,
        ge=0
    ),
    db: Session = Depends(get_db),
):
    return get_all_work_items(
        db=db,
        search=search,
        employee_id=employee_id,
        status=status.value if status else None,
        priority=priority.value if priority else None,
        limit=limit,
        offset=offset,
    )

@app.get(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def get_work_item(
    work_item_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    work_item = get_work_item_by_id(
        db,
        work_item_id
    )

    if work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    return work_item


@app.put(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def update_work_item_api(
    work_item_data: WorkItemUpdate,
    work_item_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    work_item = get_work_item_by_id(
        db,
        work_item_id
    )

    if work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    updated_work_item = update_work_item(
        db,
        work_item_id,
        work_item_data
    )
    if updated_work_item == "employee_not_found":
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if updated_work_item == "database_error":
        raise HTTPException(
            status_code=500,
            detail="Failed to update work item due to a database error"
        )

    return updated_work_item

@app.delete(
    "/work-items/{work_item_id}",
    status_code=204
)
def delete_work_item_api(
    work_item_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    work_item = get_work_item_by_id(
        db,
        work_item_id
    )

    if work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )
    deleted_work_item = delete_work_item(
        db,
        work_item_id
    )
    if deleted_work_item == "database_error":
        raise HTTPException(
            status_code=500,
            detail="Failed to delete work item due to a database error"
        )
    return None