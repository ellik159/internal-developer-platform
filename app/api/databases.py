from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

router = APIRouter()

@router.post("/")
def create_database(name: str):
    # TODO: implement postgres creation
    return {"name": name, "status": "created"}
