"""Alerts endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


@router.get("/")
def list_alerts(patient_id: Optional[int] = None,
                severity: Optional[str] = None,
                acknowledged: Optional[bool] = False):
    """List active alerts. Filter by patient, severity, or acknowledged state."""
    return []


@router.put("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, acknowledged_by: str):
    """Mark an alert as acknowledged."""
    raise HTTPException(status_code=404, detail="Alert not found")
