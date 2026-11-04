from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Employee, WorkItem
from app.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    WorkItemCreate,
    WorkItemUpdate,
    WorkItemStatus,
)
def validate_status_transition(
    current_status: str,
    requested_status: WorkItemStatus,
):
    current = WorkItemStatus(current_status)
    requested = requested_status

    # Requesting the current status is allowed.
    if current == requested:
        return True

    allowed_transitions = {
        WorkItemStatus.TODO: WorkItemStatus.IN_PROGRESS,
        WorkItemStatus.IN_PROGRESS: WorkItemStatus.COMPLETED,
    }

    return allowed_transitions.get(current) == requested

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

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return "has_work_items"

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

    try:
        db.add(new_work_item)
        db.commit()
        db.refresh(new_work_item)

        return new_work_item

    except SQLAlchemyError as e:
        db.rollback()
        print("DATABASE ERROR:", e)
        return "database_error"


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
    work_item = get_work_item_by_id(db, work_item_id)

    if work_item is None:
        return None

    # Validate the employee before changing anything.
    employee = (
        db.query(Employee)
        .filter(Employee.id == work_item_data.employee_id)
        .first()
    )

    if employee is None:
        return "employee_not_found"

    # Check the requested status before changing any fields.
    requested_status = work_item_data.status

    if requested_status is not None:
        if not validate_status_transition(
            work_item.status,
            requested_status,
        ):
            return "invalid_status_transition"

    try:
        # Update fields only after all business validations pass.
        work_item.title = work_item_data.title
        work_item.description = work_item_data.description
        work_item.employee_id = work_item_data.employee_id

        # Preserve the current status when PUT omits it.
        if requested_status is not None:
            work_item.status = requested_status.value

        work_item.priority = work_item_data.priority.value
        work_item.due_date = work_item_data.due_date

        db.commit()
        db.refresh(work_item)

        return work_item

    except SQLAlchemyError:
        db.rollback()
        return "database_error"

def update_work_item_status(
    db: Session,
    work_item_id: int,
    requested_status: WorkItemStatus,
):
    work_item = get_work_item_by_id(db, work_item_id)

    if work_item is None:
        return None

    if not validate_status_transition(
        work_item.status,
        requested_status,
    ):
        return "invalid_status_transition"

    # Don't commit or modify the record when the status is unchanged.
    if work_item.status == requested_status.value:
        return work_item

    try:
        work_item.status = requested_status.value
        db.commit()
        db.refresh(work_item)
        return work_item

    except SQLAlchemyError:
        db.rollback()
        return "database_error"

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

    try:
        db.delete(work_item)
        db.commit()

        return work_item

    except SQLAlchemyError:
        db.rollback()
        return "database_error"

def get_employee_work_summary(
    db: Session,
    employee_id: int,
):
    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        return None

    counts = (
        db.query(
            WorkItem.status,
            func.count(WorkItem.id),
        )
        .filter(WorkItem.employee_id == employee_id)
        .group_by(WorkItem.status)
        .all()
    )

    status_counts = {
        "TODO": 0,
        "IN_PROGRESS": 0,
        "COMPLETED": 0,
    }

    for status, count in counts:
        status_counts[status] = count

    total = sum(status_counts.values())

    return {
        "employee_id": employee_id,
        "total_work_items": total,
        "todo": status_counts["TODO"],
        "in_progress": status_counts["IN_PROGRESS"],
        "completed": status_counts["COMPLETED"],
    }