from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.namespace import Namespace
from app.models.user import User
from app.services.kubernetes import KubernetesService

router = APIRouter()

@router.get("/")
def list_namespaces(db: Session = Depends(get_db)):
    namespaces = db.query(Namespace).all()
    return namespaces

@router.post("/")
def create_namespace(name: str, db: Session = Depends(get_db)):
    # Check if exists
    existing = db.query(Namespace).filter(Namespace.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Namespace exists")
    
    # Create in K8s
    k8s = KubernetesService()
    k8s.create_namespace(name)
    
    # Save to DB
    namespace = Namespace(name=name)
    db.add(namespace)
    db.commit()
    
    return namespace
