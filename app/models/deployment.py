from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    namespace_id = Column(Integer, ForeignKey("namespaces.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    git_repo = Column(String)
    git_branch = Column(String, default="main")
    argocd_app_name = Column(String)
    status = Column(String, default="pending")  # pending, synced, out-of-sync, error
    sync_status = Column(JSON)
    health_status = Column(String)
    last_sync = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
