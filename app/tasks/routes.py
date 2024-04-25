from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.tasks.crud import create_task, get_task, update_task, delete_task
from app.tasks.models import Task as TaskSchema
from app.dependencies import get_db
from app.auth.models import User
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/tasks/", response_model=TaskSchema)
async def create_task(
    task: TaskSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if task.creator != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only task creator can create a task"
        )
    return create_task(db, task)

@router.get("/tasks/{task_id}/", response_model=TaskSchema)
async def read_task(task_id: UUID, db: Session = Depends(get_db)):
    task = get_task(db, str(task_id))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/tasks/{task_id}/", response_model=TaskSchema)
async def update_task(
    task_id: UUID,
    task_data: TaskSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_task = get_task(db, str(task_id))

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if existing_task.creator != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only task creator can update a task"
        )
    
    updated_task = update_task(db, str(task_id), task_data)
    return updated_task

@router.delete("/tasks/{task_id}/", response_model=TaskSchema)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_task = get_task(db, str(task_id))

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if existing_task.creator != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only task creator can delete a task"
        )
    
    deleted_task = delete_task(db, str(task_id))
    return deleted_task
