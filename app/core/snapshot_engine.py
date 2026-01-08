from app.db.models.boq_snapshot import BOQSnapshot
from app.core.hash_utils import generate_boq_hash
from app.core.gst_engine import calculate_gst


def create_boq_snapshot(
    db,
    project_id,
    component_id,
    boq_result,
    contingency_rate=0.05,
    gst_type="works_contract"
):
    """
    Finalizes pricing:
    - Adds contingency
    - Applies GST
    - Hashes BOQ
    - Persists immutable snapshot
    """

    # 1. Base subtotal (from BOQ engine)
    subtotal = float(boq_result.subtotal)

    # 2. Contingency
    contingency = round(subtotal * contingency_rate, 2)

    # 3. GST (legal layer)
    gst = calculate_gst(
        amount=subtotal + contingency,
        gst_type=gst_type
    )

    # 4. Final payable amount
    total = round(subtotal + contingency + gst, 2)

    # 5. Immutable BOQ JSON
    boq_json = boq_result.dict()

    # 6. Tamper-detection hash
    boq_hash = generate_boq_hash(boq_json)

    snapshot = BOQSnapshot(
        project_id=project_id,
        component_id=component_id,
        boq_json=boq_json,
        subtotal=subtotal,
        contingency=contingency,
        gst=gst,
        total=total,
        hash=boq_hash
    )

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot
