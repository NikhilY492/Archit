from sqlalchemy import Column, Numeric, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    project_id = Column(UUID(as_uuid=True), nullable=False)
    snapshot_id = Column(UUID(as_uuid=True), nullable=False)

    milestone = Column(String, nullable=False)
    percentage = Column(Numeric, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)

    status = Column(String, default="pending")
    paid_at = Column(TIMESTAMP, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
