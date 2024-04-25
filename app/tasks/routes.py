from fastapi import APIRouter, Depends,HTTPException, status
from app.tasks.models import Task, TaskInDB
from app.tasks.crud import create_tasks, get_task, update_task, delete_task
from app.dependecies import get_current_user
from app.auth import User
router= APIRouter()

@router.post("/tasks/", response_model=Task)
async def create_task(task: Task, current_user: User = Depends(get_current_user)):
    
    if task.creator != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only task creator can can create a task")
    return create_task(task)

@router.get("/tasks/{task_id}/", response_model=Task)
async def read_task(task_id:str):
    task= get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/tasks/{task_id}/", response_model=Task)
async def update_task(task_id:str , task_data: Task, current_user: User = Depends(get_current_user)):
    
    existing_task= get_task(task_id)

    if existing_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if existing_task.creator != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only task creator can update task")
    
    updated_task= update_task(task_id, task_data)
    return updated_task


@router.delete("/tasks/{task_id}/", response_model=Task)
async def delete_task(task_id:str , task_data: Task, current_user: User = Depends(get_current_user)):
    
    existing_task= get_task(task_id)

    if existing_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if existing_task.creator != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only task creator can delete task")
    
    deleted_task= update_task(task_id, task_data)
    return deleted_task