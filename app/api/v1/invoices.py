from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
import os

from app.api.deps import get_db
from app.db.models.boq_snapshot import BOQSnapshot
from app.db.models.invoice import Invoice
from app.db.models.project import Project

from app.core.invoice_engine import (
    calculate_invoice_amount,
    MILESTONE_SEQUENCE,
)
from app.core.pdf_engine import generate_invoice_pdf

router = APIRouter()


# ------------------------------------------------------------------
# CREATE INVOICE (WITH MILESTONE ORDER ENFORCEMENT)
# ------------------------------------------------------------------
@router.post("/invoices/{snapshot_id}/{milestone}")
def create_invoice(
    snapshot_id: UUID,
    milestone: str,
    db: Session = Depends(get_db)
):
    # 1. Fetch locked snapshot
    snapshot = (
        db.query(BOQSnapshot)
        .filter(
            BOQSnapshot.id == snapshot_id,
            BOQSnapshot.is_locked == True
        )
        .first()
    )

    if not snapshot:
        raise HTTPException(
            status_code=400,
            detail="Snapshot must be locked before invoicing"
        )

    # 2. Fetch existing invoices
    existing_invoices = (
        db.query(Invoice)
        .filter(Invoice.snapshot_id == snapshot_id)
        .all()
    )

    completed_milestones = {inv.milestone for inv in existing_invoices}

    # 3. Validate milestone
    if milestone not in MILESTONE_SEQUENCE:
        raise HTTPException(status_code=400, detail="Invalid milestone")

    requested_index = MILESTONE_SEQUENCE.index(milestone)

    # 4. Enforce milestone order
    for prior in MILESTONE_SEQUENCE[:requested_index]:
        if prior not in completed_milestones:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot create '{milestone}' invoice before '{prior}'"
            )

    # 5. Prevent duplicate invoice
    if milestone in completed_milestones:
        raise HTTPException(
            status_code=400,
            detail="Invoice for this milestone already exists"
        )

    # 6. Calculate invoice amount
    percentage, amount = calculate_invoice_amount(
        total=float(snapshot.total),
        milestone=milestone
    )

    # 7. Create invoice
    invoice = Invoice(
        project_id=snapshot.project_id,
        snapshot_id=snapshot.id,
        milestone=milestone,
        percentage=percentage,
        amount=amount
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice


# ------------------------------------------------------------------
# MARK INVOICE AS PAID
# ------------------------------------------------------------------
@router.post("/invoices/{invoice_id}/pay")
def mark_invoice_paid(
    invoice_id: UUID,
    db: Session = Depends(get_db)
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id)
        .first()
    )

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.status == "paid":
        raise HTTPException(
            status_code=400,
            detail="Invoice already marked as paid"
        )

    invoice.status = "paid"
    invoice.paid_at = datetime.utcnow()

    db.commit()
    db.refresh(invoice)

    return {
        "message": "Invoice marked as paid",
        "invoice_id": invoice.id,
        "paid_at": invoice.paid_at
    }


# ------------------------------------------------------------------
# DOWNLOAD INVOICE PDF
# ------------------------------------------------------------------
@router.get("/invoices/{invoice_id}/pdf")
def download_invoice_pdf(
    invoice_id: UUID,
    db: Session = Depends(get_db)
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id)
        .first()
    )

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    snapshot = (
        db.query(BOQSnapshot)
        .filter(BOQSnapshot.id == invoice.snapshot_id)
        .first()
    )

    project = (
        db.query(Project)
        .filter(Project.id == invoice.project_id)
        .first()
    )

    if not snapshot or not project:
        raise HTTPException(
            status_code=500,
            detail="Corrupted invoice data"
        )

    file_path = f"/mnt/data/invoice_{invoice.id}.pdf"

    generate_invoice_pdf(
        invoice=invoice,
        snapshot=snapshot,
        project=project,
        file_path=file_path
    )

    return FileResponse(
        path=file_path,
        filename=f"invoice_{invoice.id}.pdf",
        media_type="application/pdf"
    )