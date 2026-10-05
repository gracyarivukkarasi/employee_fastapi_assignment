**\*\*# FastAPI Backend Application to Manage Employees\*\***
**\*\*## Project Overview\*\***
This project is a FastAPI backend application used to manage employee
records through REST APIs.
In Task 2, the Employee Management application was extended to use a
MySQL database with SQLAlchemy for persistent data storage.
Employee records are stored in the MySQL `employees` table and remain
available even after restarting the FastAPI application.
**\*\*## Technologies Used\*\***

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

**\*\*## Features\*\***

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

**\*\*## Database Setup\*\***
**\*\*### 1. Create the MySQL Database\*\***
Open MySQL Workbench or MySQL Command Line and run:
```sql
CREATE DATABASE employee_management;
```
Verify the database:
```sql
SHOW DATABASES;
```
**\*\*### 2. Configure Database Connection\*\***
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
The `.env` file contains local database credentials and is excluded
from Git.
A `.env.example` file is provided with placeholder values.
**\*\*### 3. Create the Employees Table\*\***
The `employees` table is created automatically by SQLAlchemy when the
FastAPI application starts.
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

### 4. Create the Work Items Table

The `work_items` table is created automatically by SQLAlchemy when the
FastAPI application starts.
The table contains:

-   `id`

-   `title`

-   `description`

-   `employee_id`

-   `status`

-   `priority`

-   `due_date`

-   `created_at`

The `employee_id` column is a foreign key referencing `employees.id`.
**\*\*## Setup and Installation\*\***
**\*\*### 1. Create a Virtual Environment\*\***
```powershell
py -3.12 -m venv venv
```
**\*\*### 2. Activate the Virtual Environment\*\***
```powershell
.\venv\Scripts\Activate.ps1
```
**\*\*### 3. Install the Required Packages\*\***
```powershell
pip install -r requirements.txt
```
**\*\*### 4. Run the FastAPI Application\*\***
```powershell
uvicorn app.main:app --reload
```
**\*\*### 5. Open Swagger UI\*\***
Open the following URL in a browser:
```text
http://127.0.0.1:8000/docs
```
Swagger UI can be used to test all available API endpoints.
**\*\*## API Endpoints\*\***
| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check application health |
| POST | `/employees` | Create a new employee |
| GET | `/employees` | Get all employees |
| GET | `/employees/{employee_id}` | Get an employee by ID |
| PUT | `/employees/{employee_id}` | Update an employee |
| DELETE | `/employees/{employee_id}` | Delete an employee |
**\*\*## Task 3 -- Filtering and Pagination\*\***
The `GET /employees` endpoint was extended with optional filtering,
searching, and pagination parameters.
**\*\*### Query Parameters\*\***
| Parameter | Type | Default | Description |
|---|---|---:|---|
| `search` | string | None | Partial, case-insensitive search by
employee name |
| `department` | string | None | Filter employees by department |
| `work_mode` | WFH/WFO | None | Filter employees by work mode |
| `is_active` | boolean | None | Filter employees by active status
|
| `limit` | integer | 10 | Number of records to return. Allowed
range: 1--100 |
| `offset` | integer | 0 | Number of records to skip. Must be 0 or
greater |
Multiple filters can be used together.
**\*\*### Example Requests\*\***
Search by employee name:
```text
GET /employees?search=an
Filter by department:
GET /employees?department=Engineering
Filter by work mode:
GET /employees?work_mode=WFH
Filter by active status:
GET /employees?is_active=false
Combined filters:
GET /employees?department=Engineering&work_mode=WFH&is_active=true
Pagination:
GET /employees?limit=3&offset=0
Next page:
GET /employees?limit=3&offset=3
### Response Format
The response contains the total number of matching employees before
pagination, along with the limit, offset, and employee records.
{
  "total": 10,
  "limit": 3,
  "offset": 0,
  "items": []
}
When there are no matching employees, the API returns 200 OK with an
empty items list.
{
  "total": 0,
  "limit": 10,
  "offset": 0,
  "items": []
}
### Validation
limit must be between 1 and 100.
offset must be 0 or greater.
work_mode must be either WFH or WFO.
Invalid query parameter values return a 422 Unprocessable Entity
response.
### SQLAlchemy Filtering and Pagination
Filtering, searching, counting, ordering, and pagination are performed
using SQLAlchemy database query operations.
\\
## Task 4 -- Work Item Management
Task 4 extends the Employee Management API by adding work item
management linked to existing employees.

### Work Item and Employee Relationship

Each work item is assigned to an existing employee through the
`employee_id` foreign key.
The SQLAlchemy models use a relationship between `Employee` and
`WorkItem`:

-   One employee can have multiple work items.

-   Each work item belongs to one employee.

-   The `employee_id` column references `employees.id`.

-   Work item responses include the assigned employee's `id`, `name`,

    and `email`.

### Work Item Fields

  Field           Description
\*\*  --------------- --------------------------------------------\*\*
  `id`            Auto-generated primary key
  `title`         Required work item title
  `description`   Optional description
  `employee_id`   ID of the assigned employee
  `status`        `TODO`, `IN_PROGRESS`, or `COMPLETED`
  `priority`      `LOW`, `MEDIUM`, or `HIGH`
  `due_date`      Optional due date
  `created_at`    Automatically generated creation timestamp
Default values:

-   `status` defaults to `TODO`.

-   `priority` defaults to `MEDIUM`.

### Work Item Query Parameters

The `GET /work-items` endpoint supports:
\*\*  --------------------------------------------------------------------------------------\*\*
  Parameter        Type                                       Default Description
\*\*  ---------------- ---------------------------- --------------------- ------------------\*\*
  `search`         string                                        None Partial,
                                                                      case-insensitive
                                                                      search by work
                                                                      item title
  `employee_id`    integer                                       None Filter by assigned
                                                                      employee
  `status`         TODO/IN_PROGRESS/COMPLETED                    None Filter by status
  `priority`       LOW/MEDIUM/HIGH                               None Filter by priority
  `limit`          integer                                         10 Number of records
                                                                      to return. Allowed
                                                                      range: 1--100
  `offset`         integer                                          0 Number of records
                                                                      to skip. Must be 0
                                                                      or greater
  --------------------------------------------------------------------------------------
Multiple filters can be used together.

### Example Work Item Requests

Create a work item:

```

{

  "title": "Prepare weekly status report",

  "description": "Prepare and submit the weekly report",

  "employee_id": 2,

  "status": "TODO",

  "priority": "MEDIUM",

  "due_date": "2026-10-05"

}

```

Search by title:

```

GET /work-items?search=weekly

```

Filter by employee:

```

GET /work-items?employee_id=2

```

Filter by status:

```

GET /work-items?status=IN_PROGRESS

```

Filter by priority:

```

GET /work-items?priority=MEDIUM

```

Combined filters:

```

GET /work-items?search=weekly&employee_id=2&status=TODO&priority=MEDIUM

```

Pagination:

```

GET /work-items?limit=1&offset=0

```

### Work Item Response Format

The work item response includes the assigned employee:

```

{

  "id": 1,

  "title": "Prepare weekly status report",

  "description": "Prepare and submit the weekly report",

  "employee_id": 2,

  "status": "TODO",

  "priority": "MEDIUM",

  "due_date": "2026-10-05",

  "created_at": "2026-09-28T18:05:53",

  "assigned_employee": {

    "id": 2,

    "name": "Employee Name",

    "email": "employee@example.com"

  }

}

```

For list responses, the API returns the total number of matching work
items before pagination:

```

{

  "total": 2,

  "limit": 10,

  "offset": 0,

  "items": []

}

```

### Work Item Validation and Error Handling

-   `title` is required and cannot be empty or whitespace only.

-   `employee_id` must be greater than 0.

-   The assigned employee must exist.

-   `status` must be `TODO`, `IN_PROGRESS`, or `COMPLETED`.

-   `priority` must be `LOW`, `MEDIUM`, or `HIGH`.

-   `limit` must be between 1 and 100.

-   `offset` must be 0 or greater.

-   `404 Not Found` is returned when the employee or work item does not

    exist.

-   Invalid status, priority, title, or query parameters return

    `422 Unprocessable Entity`.

-   Successful work item creation returns `201 Created`.

-   Successful work item deletion returns `204 No Content`.

### SQLAlchemy Relationship and Persistence

The `WorkItem` model uses a foreign key to the `employees` table and a
SQLAlchemy relationship to access the assigned employee.
Work items are stored in the MySQL `work_items` table. Because the
application uses MySQL and SQLAlchemy, work item records remain
available after restarting the FastAPI application.

### Task 4 Testing

The following Task 4 scenarios were tested using Swagger UI:

-   Create work item for an existing employee

-   Create work item with a nonexistent employee

-   Get all work items

-   Get work item by ID

-   Partial and case-insensitive title search

-   Employee filter

-   Status filter

-   Priority filter

-   Combined filters

-   Pagination using limit and offset

-   Update and reassign work item

-   Invalid status validation

-   Invalid priority validation

-   Whitespace-only title validation

-   Missing work item

-   Delete work item

-   Verify deleted work item returns 404

-   Persistence after application restart

-   Existing employee API regression testing

### Task 4 Test Results

  Test Scenario                      Expected Result                         Status
\*\*  ---------------------------------- --------------------------------------- --------\*\*
  Create work item                   201 Created                             Passed
  Get all work items                 200 OK                                  Passed
  Get work item by ID                200 OK                                  Passed
  Title search                       Matching work items returned            Passed
  Employee filter                    Matching employee records returned      Passed
  Status filter                      Matching status records returned        Passed
  Priority filter                    Matching priority records returned      Passed
  Combined filters                   All selected filters applied together   Passed
  Pagination                         Correct limit and offset applied        Passed
  Update/reassign work item          200 OK with updated data                Passed
  Invalid status/priority            422 Validation Error                    Passed
  Whitespace-only title              422 Validation Error                    Passed
  Work item not found                404 Not Found                           Passed
  Delete work item                   204 No Content                          Passed
  Deleted work item verification     404 Not Found                           Passed
  Restart persistence                Work item retrieved after restart       Passed
  Existing employee API regression   200 OK                                  Passed

### Task 4 Screenshots

The `screenshots` folder should contain screenshots for the Task 4 API
and database testing results, including:

-   Create work item

-   Get all work items

-   Get work item by ID

-   Title search

-   Employee filter

-   Status filter

-   Priority filter

-   Combined filters

-   Pagination

-   Update/reassign work item

-   Invalid status/priority

-   Whitespace-only title

-   Work item not found

-   Delete work item

-   Deleted work item verification

-   Restart persistence

-   Existing employee API regression

### What I Learned in Task 4

Through Task 4, I learned:

-   How to create a related SQLAlchemy model using a foreign key.

-   How to define relationships between SQLAlchemy models.

-   How to return related employee details in an API response.

-   How to use Pydantic enums for status and priority validation.

-   How to implement work item CRUD APIs.

-   How to combine search, filters, and pagination using SQLAlchemy.

-   How to validate related employee IDs.

-   How to handle 404, 422, 201, and 204 API responses.

-   How to verify database persistence after restarting the FastAPI

    application.

-   How to test related-resource APIs using Swagger UI.

### Difficulties Faced in Task 4

During Task 4, I faced difficulties while setting up the `WorkItem`
model, connecting it to the existing `Employee` model, and returning the
assigned employee details in the response.
I resolved these issues by defining the foreign key and SQLAlchemy
relationship, adding the required Pydantic response model, checking
FastAPI validation errors, and testing the APIs step by step through
Swagger UI.

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
- A `404 Not Found` response is returned when an employee does not

exist.

- A `409 Conflict` response is returned when a duplicate email is

provided.

- Invalid request data returns a `422 Unprocessable Entity` response.

## Database Session Management
The application uses SQLAlchemy sessions for database operations.
A database session is created for each request and automatically closed
after the request is completed.
Failed database changes are rolled back to prevent the session from
remaining in a failed transaction state.
## Data Persistence
Employee records are stored in the MySQL `employee_management`
database.
All CRUD operations are performed against the MySQL database using
SQLAlchemy.
Unlike Task 1, employee records are persistent and remain available
after restarting the FastAPI application.
## Persistence Verification
An employee was created before restarting the FastAPI application.
After restarting the application, the same employee was successfully
retrieved using:
```text
GET /employees/2
```
The API returned `200 OK`, confirming that the employee record
remained available after the application restart.
**\*\*## Testing\*\***
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
- Partial and case-insensitive employee name search
- Department filter
- Work mode filter
- Active/inactive employee filter
- Combined filters
- Pagination using limit and offset
- No matching records
- Invalid limit validation
- Invalid offset validation
- Invalid work mode validation

**\*\*## Test Results\*\***
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
| Partial name search | Matching employees returned | Passed |
| Department filter | Matching department records returned | Passed
|
| Work mode filter | Matching WFH/WFO records returned | Passed |
| Active status filter | Matching active/inactive records returned |
Passed |
| Combined filters | All selected filters applied together | Passed
|
| Pagination | Correct limit and offset applied | Passed |
| No matching records | 200 OK with empty items | Passed |
| Invalid limit | 422 Validation Error | Passed |
| Invalid offset | 422 Validation Error | Passed |
| Invalid work mode | 422 Validation Error | Passed |
**\*\*## Screenshots\*\***
The `screenshots` folder contains screenshots showing the API and
database testing results.
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
- partial-name search
- department filter
- work mode filter
- active/inactive filter
- combined filters
- pagination
- no matching records
- invalid limit
- invalid offset
- invalid work mode

**\*\*## What I Learned\*\***
Through Tasks 2, 3, and 4, I learned:

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
- How to implement query parameters in FastAPI.
- How to perform partial and case-insensitive searches using

SQLAlchemy.

- How to apply multiple SQLAlchemy filters together.
- How to implement pagination using limit and offset.
- How to calculate the total number of matching records before

pagination.

- How to validate query parameters using FastAPI and Pydantic.
- How to test filtering and pagination APIs using Swagger UI.

**\*\*## Difficulties Faced\*\***
During Task 2, I faced difficulties while configuring MySQL, connecting
the FastAPI application to the database, installing SQLAlchemy and the
MySQL driver, and understanding database sessions.
I resolved these issues by checking error messages, verifying the MySQL
service and database connection, and testing the application step by
step using Swagger UI and MySQL Workbench.
During Task 3, I faced difficulties while implementing multiple query
parameters, combining SQLAlchemy filters, and handling pagination with
total record counts. I resolved these issues by implementing the filters
step by step and testing each scenario through Swagger UI, including
combined filters, pagination, no-match cases, and invalid inputs.
**\*\*## Assumptions\*\***

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
- Employee and WorkItem use a SQLAlchemy relationship through a foreign

key.

- Database migrations are not required for this assignment.

**\*\*## Error Handling\*\***
The application handles common errors including:

- `404 Not Found` for missing employees
- `409 Conflict` for duplicate emails
- `422 Unprocessable Entity` for invalid request data
- Database transaction rollback for failed database changes

**\*\*## Requirements\*\***
The required Python packages are listed in:
```text
requirements.txt
```
The application requires Python 3.12 and a running MySQL server.
**\*\*## Git\*\***
The project is maintained using Git.
Task 2, Task 3, and Task 4 changes were committed and pushed to the
existing repository with meaningful commits.
The `.env` file is excluded from Git to prevent database credentials
from being committed.