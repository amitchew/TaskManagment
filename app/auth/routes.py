from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.crud import create_user, get_user_by_username
from app.auth.security import authenticate_user, create_access_token, pwd_context
from app.dependencies import get_db
from app.auth.models import User as UserSchema
from app.database.models import User as UserDB

router = APIRouter()

@router.post("/register/", response_model=UserSchema)
async def register(user: UserSchema, db: Session = Depends(get_db)):
    
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    db_user = create_user(db, user)
    return db_user

@router.post("/login/")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(get_user_by_username(db, form_data.username), form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user/me/", response_model=UserSchema)
async def read_current_user(current_user: UserSchema = Depends(get_current_user)):
    return current_user
