from sqlalchemy.orm import Session

from app import models, schemas


def create_employee(
    db: Session,
    employee: schemas.EmployeeCreate
):
    existing_employee = (
        db.query(models.Employee)
        .filter(models.Employee.email == str(employee.email))
        .first()
    )

    if existing_employee:
        return None

    db_employee = models.Employee(
        name=employee.name,
        email=str(employee.email),
        department=employee.department,
        primary_skill=employee.primary_skill,
        location=employee.location,
        work_mode=employee.work_mode.value,
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


def get_all_employees(db: Session):
    return (
        db.query(models.Employee)
        .order_by(models.Employee.id)
        .all()
    )


def get_employee_by_id(db: Session, employee_id: int):
    return (
        db.query(models.Employee)
        .filter(models.Employee.id == employee_id)
        .first()
    )