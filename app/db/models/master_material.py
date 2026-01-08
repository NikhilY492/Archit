from sqlalchemy import Column, String, Numeric, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class MasterMaterial(Base):
    __tablename__ = "master_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    base_rate = Column(Numeric(10, 2), nullable=False)

    # economy / premium / luxury
    quality = Column(String, nullable=False)

    hsn_code = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
