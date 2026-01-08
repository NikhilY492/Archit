from sqlalchemy import Column, TIMESTAMP, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.db.base import Base

class ComponentInstance(Base):
    __tablename__ = "component_instances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"))
    component_type = Column(String, nullable=False)
    dimensions = Column(JSONB, nullable=False)
    parameters = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
