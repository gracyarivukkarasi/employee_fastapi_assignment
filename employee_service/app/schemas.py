from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class WorkMode(str, Enum):
    WFH = "WFH"
    WFO = "WFO"


class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    department: str = Field(..., min_length=1, max_length=100)
    primary_skill: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=100)
    work_mode: WorkMode

    @field_validator("name", "department", "primary_skill", "location")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be blank")
        return value


class EmployeeResponse(EmployeeCreate):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)