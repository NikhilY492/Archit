from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.component import ComponentCreate
from app.db.models.component_instance import ComponentInstance
from app.db.models.project import Project
from app.core.validation import validate_component_payload

router = APIRouter()

@router.post("/components")
def create_component(
    payload: ComponentCreate,
    db: Session = Depends(get_db)
):
    # 1. Ensure project exists
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 2. Enforce component schema
    validate_component_payload(
        component_type=payload.component_type,
        dimensions=payload.dimensions,
        parameters=payload.parameters
    )

    # 3. Persist component
    component = ComponentInstance(
        project_id=payload.project_id,
        component_type=payload.component_type,
        dimensions=payload.dimensions,
        parameters=payload.parameters
    )
    db.add(component)
    db.commit()
    db.refresh(component)
    if project.status in ("approved", "purchase_order"):
        raise HTTPException(
            status_code=403,
            detail="Cannot modify components after approval"
        )

    return component
