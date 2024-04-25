from fastapi import APIRouter, Depends,HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.models import User, UserInDB
from app.auth.security import authenticate_user, create_access_token,fake_users_db,pwd_context
from app.dependecies import get_current_user
from app.auth import User


router = APIRouter()

@router.post("/register/" ,response_model=User)
async def register(user:User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    hashed_password= pwd_context.hash(user.password)
    user_data= UserInDB(**user.dict(), hashed_password=hashed_password)

    fake_users_db[user.username]= user_data.dict()


@router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm=Depends()):
    
    user= authenticate_user(fake_users_db, form_data.user_name,form_data.password0)

    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token=create_access_token(data={"sub": user.username})
    return {"access_token": access_token,"token_type":"bearer"}


    

@router.post("/user/me/", response_model=User)
async def read_current_user(current_user:User= Depends(get_current_user)):
    return current_user
