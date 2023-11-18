from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class NamespaceBase(BaseModel):
    name: str
    description: Optional[str] = None
    team: Optional[str] = None
    labels: Optional[Dict[str, str]] = None

class NamespaceCreate(NamespaceBase):
    resource_quota: Optional[Dict] = None

class NamespaceUpdate(BaseModel):
    description: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    resource_quota: Optional[Dict] = None

class NamespaceResponse(NamespaceBase):
    id: int
    owner_id: int
    status: str
    resource_quota: Optional[Dict] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
