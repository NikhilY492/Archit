from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db
from app.db.models.component_instance import ComponentInstance
from app.db.models.master_material import MasterMaterial
from app.core.boq_engine import calculate_mirrored_cupboard
from app.core.rate_loader import load_rates

router = APIRouter()


@router.get("/boq/{component_id}")
def generate_boq(component_id: UUID, db: Session = Depends(get_db)):
    """
    Generate BOQ for a single component instance.
    Deterministic, read-only, no persistence.
    """

    # 1. Fetch component
    component = (
        db.query(ComponentInstance)
        .filter(ComponentInstance.id == component_id)
        .first()
    )

    if not component:
        raise HTTPException(
            status_code=404,
            detail="Component not found"
        )

    # 2. Load master rates
    materials = (
        db.query(MasterMaterial)
        .filter(MasterMaterial.is_active == True)
        .all()
    )

    if not materials:
        raise HTTPException(
            status_code=500,
            detail="Master material library is empty"
        )
    rate_version, materials = get_materials_for_active_version(db)

    rates = load_rates(materials)

    # 3. Route to component-specific BOQ logic
    if component.component_type == "mirrored_cupboard":
        return calculate_mirrored_cupboard(component, rates)

    # 4. Unsupported component type
    raise HTTPException(
        status_code=400,
        detail=f"BOQ not implemented for component_type: {component.component_type}"
    )
