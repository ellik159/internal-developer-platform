from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DatabaseBase(BaseModel):
    name: str
    namespace_id: int
    db_type: str = "postgresql"
    size: str = "small"

class DatabaseCreate(DatabaseBase):
    pass

class DatabaseResponse(DatabaseBase):
    id: int
    owner_id: int
    host: Optional[str] = None
    port: Optional[int] = None
    database_name: Optional[str] = None
    username: Optional[str] = None
    connection_secret: Optional[str] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class SecretCreate(BaseModel):
    name: str
    namespace: str
    data: dict  # key-value pairs

class SecretResponse(BaseModel):
    name: str
    namespace: str
    keys: list  # don't return actual values
