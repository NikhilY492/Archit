from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db
from app.db.models.project import Project
from app.db.models.boq_snapshot import BOQSnapshot
from app.db.models.invoice import Invoice
from app.core.project_finance_engine import compute_project_financials

router = APIRouter()


@router.get("/projects/{project_id}/financials")
def project_financial_summary(
    project_id: UUID,
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    snapshots = (
        db.query(BOQSnapshot)
        .filter(
            BOQSnapshot.project_id == project_id,
            BOQSnapshot.is_locked == True
        )
        .all()
    )

    invoices = (
        db.query(Invoice)
        .filter(Invoice.project_id == project_id)
        .all()
    )

    return compute_project_financials(
        snapshots=snapshots,
        invoices=invoices
    )
