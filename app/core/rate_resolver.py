from fastapi import HTTPException
from app.db.models.rate_version import RateVersion
from app.db.models.master_material import MasterMaterial


def get_active_rate_version(db):
    active_version = (
        db.query(RateVersion)
        .filter(RateVersion.is_active == True)
        .first()
    )

    if not active_version:
        raise HTTPException(
            status_code=500,
            detail="No active rate version found"
        )

    return active_version


def get_materials_for_active_version(db):
    active_version = get_active_rate_version(db)

    materials = (
        db.query(MasterMaterial)
        .filter(
            MasterMaterial.rate_version_id == active_version.id,
            MasterMaterial.is_active == True
        )
        .all()
    )

    if not materials:
        raise HTTPException(
            status_code=500,
            detail="No materials found for active rate version"
        )

    return active_version, materials
