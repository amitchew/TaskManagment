from sqlalchemy.orm import Session
from app.tasks.models import Task as TaskSchema
from app.database.models import Task
from uuid import uuid4


def create_task(db: Session, task_data: TaskSchema) -> Task:
    task_id = str(uuid4())
    db_task = Task(id=task_id, title=task_data.title, description=task_data.description,
                   due_date=task_data.due_date, status=task_data.status,
                   creator=task_data.creator, assigned_to=task_data.assigned_to)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: str) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: str, task_data: TaskSchema) -> Task:
    existing_task = get_task(db, task_id)
    if not existing_task:
        return None

    existing_task.title = task_data.title
    existing_task.description = task_data.description
    existing_task.due_date = task_data.due_date
    existing_task.status = task_data.status
    existing_task.assigned_to = task_data.assigned_to
    db.commit()
    db.refresh(existing_task)
    return existing_task


def delete_task(db: Session, task_id: str) -> Task:
    existing_task = get_task(db, task_id)
    if not existing_task:
        return None
    
    db.delete(existing_task)
    db.commit()
    return existing_task
