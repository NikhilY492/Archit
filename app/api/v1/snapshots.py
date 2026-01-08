from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db
from app.db.models.component_instance import ComponentInstance
from app.core.rate_resolver import get_materials_for_active_version
from app.core.rate_loader import load_rates
from app.core.boq_engine import calculate_mirrored_cupboard
from app.core.snapshot_engine import create_boq_snapshot

router = APIRouter()


@router.post("/snapshots/{component_id}")
def create_snapshot(
    component_id: UUID,
    db: Session = Depends(get_db)
):
    # 1. Fetch component
    component = (
        db.query(ComponentInstance)
        .filter(ComponentInstance.id == component_id)
        .first()
    )

    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    # 2. Resolve active rate version + materials (THIS is where db exists)
    rate_version, materials = get_materials_for_active_version(db)

    rates = load_rates(materials)

    # 3. Calculate BOQ
    if component.component_type != "mirrored_cupboard":
        raise HTTPException(
            status_code=400,
            detail="Unsupported component type"
        )

    boq_result = calculate_mirrored_cupboard(component, rates)

    # 4. Create immutable snapshot
    snapshot = create_boq_snapshot(
        db=db,
        project_id=component.project_id,
        component_id=component.id,
        boq_result=boq_result
    )

    return snapshot
