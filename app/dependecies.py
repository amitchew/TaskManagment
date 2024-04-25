from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.base import SessionLocal
from app.auth.security import decode_access_token
from fastapi import HTTPException, status
from jose import JWTError
from app.auth.crud import get_user_by_username


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(), db: Session = Depends(get_db)):
    try:
        username = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
