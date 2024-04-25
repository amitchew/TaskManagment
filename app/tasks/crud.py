from uuid import UUID , uuid4
from typing import Dict, Optional
from app.tasks.models import Task, TaskInDB

fake_tasks_db: Dict[str, TaskInDB] = {}

def create_task(task_data: Task)-> TaskInDB:
    task_id = str(uuid4())
    task_in_db= TaskInDB(**task_data.dict(), id= task_id)
    fake_tasks_db[task_id]= task_in_db

    return task_in_db

def get_task(task_id:str)-> Optional[TaskInDB]:
    return fake_tasks_db.get(task_id)

def update_task(task_id:str, task_data:Task)-> Optional[TaskInDB]:
    if task_id not in fake_tasks_db:
        return None
    updated_task= TaskInDB(**task_data.dict(), id= task_id)
    fake_tasks_db[task_id]=updated_task
    return updated_task


def delete_task(task_id:str)-> Optional[TaskInDB]:
    if task_id not in fake_tasks_db:
        return None
    deleted_task= fake_tasks_db.pop(task_id)
    return deleted_task