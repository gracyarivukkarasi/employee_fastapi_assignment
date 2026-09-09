# FastAPI Backend Application to Manage Employees

## Project Overview

This project is a FastAPI backend application used to manage employee records. It provides REST APIs to create, view, update, and delete employee information.

Employee data is temporarily stored in a Python list, so no database is used in this project.

## Technologies Used

- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- Swagger UI
- Git

## Features

- Create a new employee
- View all employees
- View an employee by ID
- Update employee details
- Delete an employee
- Check application health
- Validate employee input
- Ensure email addresses are unique
- Restrict work mode to WFH or WFO
- Return appropriate HTTP error responses

## Setup and Installation

### 1. Create a virtual environment
py -3.12 -m venv venv

### 2. Activate the virtual environment

.\venv\Scripts\Activate.ps1

### 3. Install the required packages
pip install -r requirements.txt

### 4. Run the FastAPI application
uvicorn app.main:app --reload

### 5. Open Swagger UI
http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check application health |
| POST | `/employees` | Create a new employee |
| GET | `/employees` | Get all employees |
| GET | `/employees/{employee_id}` | Get an employee by ID |
| PUT | `/employees/{employee_id}` | Update an employee |
| DELETE | `/employees/{employee_id}` | Delete an employee |

## Validation Rules

- Employee name is required.
- Email must be in a valid email format.
- Email addresses must be unique.
- Department is required.
- Primary skill is required.
- Location is required.
- Work mode must be either `WFH` or `WFO`.
- Employee ID must be greater than 0.
- A `404 Not Found` response is returned when an employee does not exist.
- A `409 Conflict` response is returned when a duplicate email is provided.
- Invalid input returns a validation error.

## Data Storage

Employee records are stored temporarily in a Python list in memory.

No database is used in this project. Because the data is stored in memory, all employee records are lost when the application is restarted.

## What I Learned

Through this project, I learned:

- How to create REST APIs using FastAPI.
- How to define and validate request data using Pydantic.
- How to use HTTP methods such as GET, POST, PUT, and DELETE.
- How to create CRUD operations.
- How to handle errors using `HTTPException`.
- How to use Swagger UI to test APIs.
- How to organize a FastAPI project into separate files.
- How to use a Python list for temporary data storage.
- How to create and use a virtual environment.
- How to manage project dependencies using `requirements.txt`.

## Difficulties Faced

During the development of this project, I faced some difficulties while installing the required packages, and understanding how FastAPI, Pydantic validation, and API endpoints work.

I resolved these issues by checking error messages, understanding the purpose of each component, and testing the APIs using Swagger UI.

## Assumptions

- Employee IDs are generated automatically by the application.
- Employee data is stored only in memory using a Python list.
- Employee data is lost when the application is restarted.
- No authentication or authorization is implemented.
- No database is used.
- No frontend is included in this project.

## Testing

The APIs were tested using Swagger UI available at:

http://127.0.0.1:8000/docs

The following scenarios were tested:

Health check
Create employee
Get all employees
Get employee by ID
Update employee
Delete employee
Duplicate email validation
Employee not found (404)
Invalid email validation
Invalid work mode validation
Invalid employee ID validation