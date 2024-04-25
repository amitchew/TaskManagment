from fastapi import Depends, Depends,HTTPException, status
from app.auth.models import User
from app.tasks.crud import create_tasks, get_task, update_task, delete_task
from app.dependecies import get_current_user

from fastapi.security import OAuth2PasswordBearer, decode_access_token

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token:str = Depends(oauth2_scheme))-> User:
    username= decode_access_token(token)

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Invald authentication credentials ",
            headers={"WWW-Authenticate":"Bearer"},
        )
    return User(username=username)

async def get_current_task_owner(current_user: User= Depends(get_current_user))->User:
    return current_user

