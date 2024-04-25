from passlib.context import CryptoContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.auth.models import UserinDB

pwd_context=CryptoContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY ="123456"
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_MINTES=30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict,expires_delta: timedelta=None):
    to_encode= data.copy()
    if expires_delta:
        expire=datetime.utcnow()+ expires_delta
    else:
        expire= datetime.utcnow()+ timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return encoded_jwt

def decode_access_token(token:str):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get("sub")

        if username is None:
            raise JWTError
        return username
    except JWTError:
        return None
    
def authenticated_uses(fajke_db,username:str, password:str):
    user= get_user(fajke_db,username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def get_user(fake_db, username:str):
    if username in fake_db:
        user_dict=fake_db[username]
        return UserinDB(**user_dict)

        

