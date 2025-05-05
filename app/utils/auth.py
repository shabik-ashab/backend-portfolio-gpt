from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.models.user import User
from app.db.session import SessionLocal
from datetime import datetime
import os

# OAuth2PasswordBearer is used to extract the token from the request's Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv("AUTH_SECRET")
ALGORITHM = "HS256"

def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        db.close()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
