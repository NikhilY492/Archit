from pydantic import BaseModel
from typing import Dict, Any
from uuid import UUID

class ComponentCreate(BaseModel):
    project_id: UUID
    component_type: str
    dimensions: Dict[str, Any]
    parameters: Dict[str, Any]
