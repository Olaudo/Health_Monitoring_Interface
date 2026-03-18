"""VitalWatch — Pydantic request/response schemas"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class HospitalRegister(BaseModel):
    name: str
    slug: str                  # e.g. "st-marys-london" — becomes part of login
    city: str
    country: str
    admin_email: str
    admin_password: str
    admin_first_name: str
    admin_last_name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class StaffCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    role: str = "nurse"        # nurse | doctor | admin


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: Optional[str] = None
    bed_number: str
    ward: str
    diagnosis: Optional[str] = None
    attending: Optional[str] = None
    mrn: Optional[str] = None


class VitalsCreate(BaseModel):
    patient_id: int
    heart_rate: Optional[float] = None
    spo2: Optional[float] = None
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    respiratory_rate: Optional[float] = None
    temperature: Optional[float] = None
    recorded_by: Optional[str] = "dashboard"
