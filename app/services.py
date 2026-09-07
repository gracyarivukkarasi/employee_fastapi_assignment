from datetime import datetime
from app.schemas import Employee, EmployeeCreate, EmployeeUpdate

employees: list[Employee] = []
next_employee_id = 1
def create_employee(employee: EmployeeCreate):

    global next_employee_id

    for existing_employee in employees:
        if existing_employee.email == employee.email:
            return None

    new_employee = Employee(
        id=next_employee_id,
        name=employee.name,
        email=employee.email,
        department=employee.department,
        primary_skill=employee.primary_skill,
        location=employee.location,
        work_mode=employee.work_mode,
        is_active=True,
        created_at=datetime.now()
    )
    employees.append(new_employee)
    next_employee_id += 1
    return new_employee
def get_all_employees():
    return employees

def get_employee_by_id(employee_id: int):
    for employee in employees:
        if employee.id == employee_id:
            return employee

    return None

def update_employee(employee_id: int, employee_data: EmployeeUpdate):

    for existing_employee in employees:
        if existing_employee.email == employee_data.email and existing_employee.id != employee_id:
            return None

    for employee in employees:
        if employee.id == employee_id:
            employee.name = employee_data.name
            employee.email = employee_data.email
            employee.department = employee_data.department
            employee.primary_skill = employee_data.primary_skill
            employee.location = employee_data.location
            employee.work_mode = employee_data.work_mode
            employee.is_active = employee_data.is_active

            return employee

    return None

def delete_employee(employee_id: int):
    for employee in employees:
        if employee.id == employee_id:
            employees.remove(employee)
            return employee

    return None