from sqlalchemy.orm import Session

from app import models, schemas


def create_work_item(
    db: Session,
    work_item: schemas.WorkItemCreate,
):
    db_work_item = models.WorkItem(
        title=work_item.title,
        description=work_item.description,
        employee_id=work_item.employee_id,
        status=work_item.status.value,
    )

    db.add(db_work_item)
    db.commit()
    db.refresh(db_work_item)

    return db_work_item


def get_all_work_items(db: Session):
    return (
        db.query(models.WorkItem)
        .order_by(models.WorkItem.id)
        .all()
    )


def get_work_item_by_id(
    db: Session,
    work_item_id: int,
):
    return (
        db.query(models.WorkItem)
        .filter(models.WorkItem.id == work_item_id)
        .first()
    )