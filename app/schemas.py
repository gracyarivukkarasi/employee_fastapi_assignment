from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator


class WorkMode(str, Enum):
    WFH = "WFH"
    WFO = "WFO"


class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    department: str = Field(..., min_length=1)
    primary_skill: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    work_mode: WorkMode

    @field_validator("name", "department", "primary_skill", "location")
    @classmethod
    def validate_required_fields(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return value.strip()


class EmployeeUpdate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    department: str = Field(..., min_length=1)
    primary_skill: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    work_mode: WorkMode
    is_active: bool

    @field_validator("name", "department", "primary_skill", "location")
    @classmethod
    def validate_required_fields(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return value.strip()


class EmployeeResponse(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: WorkMode
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class EmployeeListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[EmployeeResponse]