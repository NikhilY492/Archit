from sqlalchemy import Column, Numeric, Boolean, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class BOQSnapshot(Base):
    __tablename__ = "boq_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    project_id = Column(UUID(as_uuid=True), nullable=False)
    component_id = Column(UUID(as_uuid=True), nullable=False)

    boq_json = Column(JSONB, nullable=False)

    subtotal = Column(Numeric(12, 2), nullable=False)
    contingency = Column(Numeric(12, 2), nullable=False)
    gst = Column(Numeric(12, 2), nullable=False)
    total = Column(Numeric(12, 2), nullable=False)

    hash = Column(Text, nullable=False)
    is_locked = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
