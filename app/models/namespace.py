from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from app.core.database import Base

class Namespace(Base):
    __tablename__ = "namespaces"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    team = Column(String)
    description = Column(String)
    labels = Column(JSON)
    status = Column(String, default="active")
