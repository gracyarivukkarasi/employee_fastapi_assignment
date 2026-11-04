from datetime import datetime

from sqlalchemy import (
    Boolean,Column,Date,DateTime,ForeignKey,Integer,String,UniqueConstraint,
)

from sqlalchemy.orm import relationship

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
    work_items = relationship("WorkItem", back_populates="employee")

class WorkItem(Base):
    __tablename__ = "work_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    status = Column(String(20), default="TODO", nullable=False)
    priority = Column(String(20), default="MEDIUM", nullable=False)

    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    employee = relationship(
        "Employee",
        back_populates="work_items"
    )

    @property
    def assigned_employee(self):
        return self.employee