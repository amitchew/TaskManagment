from pydantic import BaseModel
from typing import Optional
from datetime import date

class Task(BaseModel):
    title:str
    description: str
    due_date: date
    status: str
    creator: str
    assigned_to: Optional[str]= None

class TaskInDB(Task):
    id: str