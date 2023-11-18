from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Database(Base):
    __tablename__ = "databases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    namespace_id = Column(Integer, ForeignKey("namespaces.id"))
    db_type = Column(String, default="postgresql")  # postgresql, mysql, etc
    host = Column(String)
    port = Column(Integer)
    database_name = Column(String)
    username = Column(String)
    connection_secret = Column(String)  # k8s secret name with credentials
    size = Column(String, default="small")  # small, medium, large
    status = Column(String, default="provisioning")  # provisioning, ready, error
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
