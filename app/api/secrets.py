from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.vault import VaultService

router = APIRouter()

@router.post("/")
def store_secret(path: str, data: dict):
    vault = VaultService()
    vault.store_secret(path, data)
    return {"status": "stored"}
