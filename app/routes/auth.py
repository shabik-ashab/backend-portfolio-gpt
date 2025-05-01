from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import UserRegister, UserLogin, Token
from app.db.session import get_db
from app.services.auth import register_user, authenticate_user
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UserRegister, db: Session = Depends(get_db)):
    new_user = register_user(db, user.name, user.email, user.password)
    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}
