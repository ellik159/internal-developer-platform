from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.user import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "dev-secret"  # TODO: move to config
ALGORITHM = "HS256"

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    # TODO: implement real auth
    user = db.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # TODO: check password
    token = jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
