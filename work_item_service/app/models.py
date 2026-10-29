from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class WorkItem(Base):
    __tablename__ = "work_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String(200), nullable=False)

    description = Column(Text, nullable=True)

    employee_id = Column(Integer, nullable=False, index=True)

    status = Column(String(20), nullable=False, default="TODO")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)