from fastapi import FastAPI
from app.api.v1.components import router as component_router
from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.session import engine
from app.api.v1.boq import router as boq_router
from app.api.v1.invoices import router as invoice_router
# DEV ONLY
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Quotation Engine")
from app.api.v1.snapshots import router as snapshot_router
from app.api.v1.projects import router as project_router

app.include_router(project_router, prefix="/api/v1")

app.include_router(snapshot_router, prefix="/api/v1")
app.include_router(invoice_router, prefix="/api/v1")
app.include_router(component_router, prefix="/api/v1")
app.include_router(boq_router, prefix="/api/v1")
@app.get("/")
def health_check():
    return {"status": "Quotation Engine running"}
