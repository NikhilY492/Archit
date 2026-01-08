from sqlalchemy import Column, String, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class RateVersion(Base):
    __tablename__ = "rate_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
