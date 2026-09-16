# FastAPI Backend Application to Manage Employees

## Project Overview

This project is a FastAPI backend application used to manage employee records through REST APIs.

In Task 2, the Employee Management application was extended to use a MySQL database with SQLAlchemy for persistent data storage.

Employee records are stored in the MySQL `employees` table and remain available even after restarting the FastAPI application.

## Technologies Used

- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy
- MySQL
- PyMySQL
- python-dotenv
- Uvicorn
- Swagger UI
- Git

## Features

- Create a new employee
- Get all employees
- Get an employee by ID
- Update employee details
- Delete an employee
- Check application health
- Store employee records in MySQL
- Use SQLAlchemy for database operations
- Automatically generate employee IDs
- Set `is_active` to `true` by default
- Generate `created_at` when an employee is created
- Preserve `created_at` during updates
- Validate employee input
- Check email uniqueness case-insensitively
- Enforce email uniqueness at the database level
- Handle database errors and failed transactions
- Close database sessions after use

## Database Setup

### 1. Create the MySQL Database

Open MySQL Workbench or MySQL Command Line and run:

```sql
CREATE DATABASE employee_management;
```

Verify the database:

```sql
SHOW DATABASES;
```

### 2. Configure Database Connection

Create a `.env` file in the project root directory.

Add the following:

```env
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=employee_management
```

Replace `your_mysql_password` with your local MySQL password.

The `.env` file contains local database credentials and is excluded from Git.

A `.env.example` file is provided with placeholder values.

### 3. Create the Employees Table

The `employees` table is created automatically by SQLAlchemy when the FastAPI application starts.

The table contains the following fields:

- `id`
- `name`
- `email`
- `department`
- `primary_skill`
- `location`
- `work_mode`
- `is_active`
- `created_at`

The employee ID is generated automatically by MySQL.

The email column has a unique database constraint.

## Setup and Installation

### 1. Create a Virtual Environment

```powershell
py -3.12 -m venv venv
```

### 2. Activate the Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install the Required Packages

```powershell
pip install -r requirements.txt
```

### 4. Run the FastAPI Application

```powershell
uvicorn app.main:app --reload
```

### 5. Open Swagger UI

Open the following URL in a browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all available API endpoints.

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
- Department is required.
- Primary skill is required.
- Location is required.
- Required text fields cannot be empty or contain only whitespace.
- Email must be in a valid email format.
- Email addresses must be unique.
- Email uniqueness is checked case-insensitively.
- Email uniqueness is also enforced at the database level.
- Work mode must be either `WFH` or `WFO`.
- Employee ID must be greater than 0.
- A `404 Not Found` response is returned when an employee does not exist.
- A `409 Conflict` response is returned when a duplicate email is provided.
- Invalid request data returns a `422 Unprocessable Entity` response.

## Database Session Management

The application uses SQLAlchemy sessions for database operations.

A database session is created for each request and automatically closed after the request is completed.

Failed database changes are rolled back to prevent the session from remaining in a failed transaction state.

## Data Persistence

Employee records are stored in the MySQL `employee_management` database.

All CRUD operations are performed against the MySQL database using SQLAlchemy.

Unlike Task 1, employee records are persistent and remain available after restarting the FastAPI application.

## Persistence Verification

An employee was created before restarting the FastAPI application.

After restarting the application, the same employee was successfully retrieved using:

```text
GET /employees/2
```

The API returned `200 OK`, confirming that the employee record remained available after the application restart.

## Testing

The APIs were tested using Swagger UI and MySQL Workbench.

The following scenarios were tested:

- Health check
- Create employee
- Get all employees
- Get employee by ID
- Update employee
- Delete employee
- Duplicate email during creation
- Case-insensitive duplicate email during update
- Employee not found
- Whitespace-only validation
- `is_active` default value
- `created_at` preservation during update
- Data persistence after application restart
- Database verification using MySQL Workbench

## Test Results

| Test Scenario | Expected Result | Status |
|---|---|---|
| Create employee | 201 Created | Passed |
| Get all employees | 200 OK | Passed |
| Get employee by ID | 200 OK | Passed |
| Update employee | 200 OK | Passed |
| Delete employee | Successful deletion | Passed |
| Duplicate email | 409 Conflict | Passed |
| Case-insensitive duplicate email | 409 Conflict | Passed |
| Employee not found | 404 Not Found | Passed |
| Whitespace-only field | 422 Validation Error | Passed |
| `is_active` default | `true` | Passed |
| `created_at` preservation | Creation time unchanged | Passed |
| Restart persistence | Employee retrieved after restart | Passed |
| MySQL database verification | Record stored in database | Passed |

## Screenshots

The `screenshots` folder contains screenshots showing the API and database testing results.

The screenshots include:

- Health check
- Employee creation
- Get all employees
- Get employee by ID
- Update employee
- Delete employee
- Duplicate email during creation
- Duplicate email during update
- Employee not found
- Whitespace validation
- Restart persistence
- `created_at` preservation
- `is_active` default
- MySQL database verification

## What I Learned

Through Task 2, I learned:

- How to connect FastAPI with MySQL.
- How to use SQLAlchemy for database operations.
- How to define database models using SQLAlchemy.
- How to perform CRUD operations using a database.
- How to manage SQLAlchemy database sessions.
- How to use environment variables for database configuration.
- How to use `.env` and `.env.example` files.
- How to create database-level unique constraints.
- How to perform case-insensitive email validation.
- How to handle database errors and roll back failed transactions.
- How to test APIs using Swagger UI.
- How to verify database records using MySQL Workbench.
- How database persistence works across application restarts.

## Difficulties Faced

During Task 2, I faced difficulties while configuring MySQL, connecting the FastAPI application to the database, installing SQLAlchemy and the MySQL driver, and understanding database sessions.

I resolved these issues by checking error messages, verifying the MySQL service and database connection, and testing the application step by step using Swagger UI and MySQL Workbench.

## Assumptions

- MySQL is installed and running locally.
- The database is named `employee_management`.
- Database credentials are stored in the local `.env` file.
- The `.env` file is not committed to Git.
- `.env.example` contains placeholder database configuration.
- Employee IDs are generated automatically by MySQL.
- Fictional employee data is used for testing.
- No authentication or authorization is implemented.
- No frontend is included.
- No Docker configuration is included.
- No relationships are required.
- Database migrations are not required for this assignment.

## Error Handling

The application handles common errors including:

- `404 Not Found` for missing employees
- `409 Conflict` for duplicate emails
- `422 Unprocessable Entity` for invalid request data
- Database transaction rollback for failed database changes

## Requirements

The required Python packages are listed in:

```text
requirements.txt
```

The application requires Python 3.12 and a running MySQL server.

## Git

The project is maintained using Git.

Task 2 changes were committed and pushed to the existing repository with meaningful commits.

The `.env` file is excluded from Git to prevent database credentials from being committed.
