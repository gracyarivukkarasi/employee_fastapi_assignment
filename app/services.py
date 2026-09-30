from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Employee, WorkItem
from app.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    WorkItemCreate,
    WorkItemUpdate,
)

def create_employee(db: Session, employee_data: EmployeeCreate):

    existing_employee = (
        db.query(Employee)
        .filter(func.lower(Employee.email) == employee_data.email.lower())
        .first()
    )

    if existing_employee:
        return None

    new_employee = Employee(
        name=employee_data.name,
        email=employee_data.email,
        department=employee_data.department,
        primary_skill=employee_data.primary_skill,
        location=employee_data.location,
        work_mode=employee_data.work_mode.value,
        is_active=True,
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


def get_all_employees(
    db: Session,
    search: str | None = None,
    department: str | None = None,
    work_mode: str | None = None,
    is_active: bool | None = None,
    limit: int = 10,
    offset: int = 0,
):
    query = db.query(Employee)

    # Search by employee name - partial and case-insensitive
    if search:
        query = query.filter(
            Employee.name.ilike(f"%{search}%")
        )

    # Filter by department
    if department:
        query = query.filter(
            Employee.department == department
        )

    # Filter by work mode
    if work_mode:
        query = query.filter(
            Employee.work_mode == work_mode
        )

    # Filter by active status
    if is_active is not None:
        query = query.filter(
            Employee.is_active == is_active
        )

    # Count matching employees BEFORE pagination
    total = query.with_entities(
        func.count(Employee.id)
    ).scalar()

    # Apply ordering and pagination through SQLAlchemy
    employees = (
        query
        .order_by(Employee.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": employees,
    }


def get_employee_by_id(db: Session, employee_id: int):

    return (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate
):

    existing_employee = (
        db.query(Employee)
        .filter(
            func.lower(Employee.email) == employee_data.email.lower(),
            Employee.id != employee_id
        )
        .first()
    )

    if existing_employee:
        return None

    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        return None

    employee.name = employee_data.name
    employee.email = employee_data.email
    employee.department = employee_data.department
    employee.primary_skill = employee_data.primary_skill
    employee.location = employee_data.location
    employee.work_mode = employee_data.work_mode.value
    employee.is_active = employee_data.is_active

    db.commit()
    db.refresh(employee)

    return employee


def delete_employee(db: Session, employee_id: int):

    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        return None

    db.delete(employee)
    db.commit()

    return employee

def create_work_item(
    db: Session,
    work_item_data: WorkItemCreate
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == work_item_data.employee_id)
        .first()
    )

    if employee is None:
        return None

    new_work_item = WorkItem(
        title=work_item_data.title,
        description=work_item_data.description,
        employee_id=work_item_data.employee_id,
        status=work_item_data.status.value,
        priority=work_item_data.priority.value,
        due_date=work_item_data.due_date,
    )

    db.add(new_work_item)
    db.commit()
    db.refresh(new_work_item)

    return new_work_item


def get_all_work_items(
    db: Session,
    search: str | None = None,
    employee_id: int | None = None,
    status: str | None = None,
    priority: str | None = None,
    limit: int = 10,
    offset: int = 0,
):
    query = db.query(WorkItem)

    if search:
        query = query.filter(
            WorkItem.title.ilike(f"%{search}%")
        )

    if employee_id is not None:
        query = query.filter(
            WorkItem.employee_id == employee_id
        )

    if status:
        query = query.filter(
            WorkItem.status == status
        )

    if priority:
        query = query.filter(
            WorkItem.priority == priority
        )

    total = query.with_entities(
        func.count(WorkItem.id)
    ).scalar()

    work_items = (
        query
        .order_by(WorkItem.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": work_items,
    }


def get_work_item_by_id(
    db: Session,
    work_item_id: int
):
    return (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )


def update_work_item(
    db: Session,
    work_item_id: int,
    work_item_data: WorkItemUpdate
):
    work_item = get_work_item_by_id(
        db,
        work_item_id
    )

    if work_item is None:
        return None

    employee = (
        db.query(Employee)
        .filter(Employee.id == work_item_data.employee_id)
        .first()
    )

    if employee is None:
        return "employee_not_found"

    work_item.title = work_item_data.title
    work_item.description = work_item_data.description
    work_item.employee_id = work_item_data.employee_id
    work_item.status = work_item_data.status.value
    work_item.priority = work_item_data.priority.value
    work_item.due_date = work_item_data.due_date

    db.commit()
    db.refresh(work_item)

    return work_item


def delete_work_item(
    db: Session,
    work_item_id: int
):
    work_item = get_work_item_by_id(
        db,
        work_item_id
    )

    if work_item is None:
        return None

    db.delete(work_item)
    db.commit()

    return work_item