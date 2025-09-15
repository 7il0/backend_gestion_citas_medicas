from pydantic import BaseModel, Field
from datetime import datetime

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    specialty_id: int
    appointment_type_id: int
    starts_at: datetime   # ISO 8601, ej: 2025-09-30T09:00:00
    duration_minutes: int = Field(default=30, ge=5, le=180)

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    specialty_id: int
    appointment_type_id: int
    starts_at: datetime
    ends_at: datetime
    status: str

    class Config:
        from_attributes = True
