"""Vitals endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


class VitalsCreate(BaseModel):
    patient_id: int
    heart_rate: Optional[float] = None
    spo2: Optional[float] = None
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    respiratory_rate: Optional[float] = None
    temperature: Optional[float] = None
    recorded_by: Optional[str] = None


class VitalsOut(VitalsCreate):
    id: int
    recorded_at: datetime

    class Config:
        from_attributes = True


@router.get("/{patient_id}")
def get_vitals(patient_id: int, hours: int = 24, limit: int = 500):
    """
    Return vitals history for a patient.
    Query params: hours (default 24), limit (default 500)
    """
    return []


@router.post("/", response_model=VitalsOut, status_code=201)
def submit_vitals(vitals: VitalsCreate):
    """
    Submit a new vitals reading. Also triggers alert_engine evaluation.
    """
    raise HTTPException(status_code=501, detail="Connect a database to enable writes")
