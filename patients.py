"""Patients CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


class PatientCreate(BaseModel):
    mrn: str
    first_name: str
    last_name: str
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    bed_number: str
    ward: str = "ICU-A"
    attending_physician: Optional[str] = None
    notes: Optional[str] = ""


class PatientOut(PatientCreate):
    id: int
    status: str
    admitted_at: datetime

    class Config:
        from_attributes = True


@router.get("/", response_model=list[PatientOut])
def list_patients(ward: Optional[str] = None, status: Optional[str] = None):
    """
    List all patients. Optionally filter by ward or status.
    Replace stub with: db.query(Patient).filter(...).all()
    """
    return []


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int):
    """Get a single patient by ID."""
    raise HTTPException(status_code=404, detail="Patient not found")


@router.post("/", response_model=PatientOut, status_code=201)
def create_patient(patient: PatientCreate):
    """Admit a new patient."""
    raise HTTPException(status_code=501, detail="Connect a database to enable writes")


@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, patient: PatientCreate):
    """Update patient record."""
    raise HTTPException(status_code=404, detail="Patient not found")


@router.delete("/{patient_id}", status_code=204)
def discharge_patient(patient_id: int):
    """Discharge (soft-delete) a patient."""
    raise HTTPException(status_code=404, detail="Patient not found")
