from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, UniqueConstraint

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    department = Column(String(100), nullable=False)
    primary_skill = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    work_mode = Column(String(10), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    __table_args__ = (
        UniqueConstraint("email", name="uq_employee_email"),
    )