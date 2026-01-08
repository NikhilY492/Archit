from app.db.models.project import Project
from app.db.models.boq_snapshot import BOQSnapshot

@router.post("/projects/{project_id}/approve")
def approve_project(project_id: UUID, db: Session = Depends(get_db)):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.status != "sent":
        raise HTTPException(
            status_code=400,
            detail="Project not ready for approval"
        )

    # Lock all snapshots
    snapshots = (
        db.query(BOQSnapshot)
        .filter(BOQSnapshot.project_id == project_id)
        .all()
    )

    for snap in snapshots:
        snap.is_locked = True

    project.status = "approved"
    db.commit()

    return {"message": "Project approved and pricing locked"}
