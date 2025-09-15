from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, date, time, timedelta
from app.db.session import SessionLocal
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.schemas.doctor import DoctorCreate, DoctorOut
from app.schemas.availability import AvailabilityOut, Slot

router = APIRouter(prefix="/medicos", tags=["medicos"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("", response_model=DoctorOut, status_code=status.HTTP_201_CREATED)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db)):
    if payload.work_end_hour <= payload.work_start_hour:
        raise HTTPException(400, "work_end_hour debe ser mayor a work_start_hour")
    obj = Doctor(
        full_name=payload.full_name,
        specialty_id=payload.specialty_id,
        work_start_hour=payload.work_start_hour,
        work_end_hour=payload.work_end_hour,
        slot_minutes=payload.slot_minutes
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("", response_model=list[DoctorOut])
def list_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).order_by(Doctor.full_name.asc()).all()

@router.get("/{doctor_id}/disponibilidad", response_model=AvailabilityOut)
def doctor_availability(doctor_id: int, fecha: str = Query(..., description="YYYY-MM-DD"),
                        db: Session = Depends(get_db)):
    doctor = db.query(Doctor).get(doctor_id)
    if not doctor:
        raise HTTPException(404, "Médico no encontrado")

    try:
        d = date.fromisoformat(fecha)
    except ValueError:
        raise HTTPException(400, "Fecha inválida, use YYYY-MM-DD")

    start_dt = datetime.combine(d, time(doctor.work_start_hour, 0))
    end_dt   = datetime.combine(d, time(doctor.work_end_hour, 0))
    step = timedelta(minutes=doctor.slot_minutes)

    taken = db.query(Appointment).filter(
        and_(
            Appointment.doctor_id == doctor_id,
            func.date(Appointment.starts_at) == d
        )
    ).all()

    slots = []
    cur = start_dt
    while cur + step <= end_dt:
        cur_end = cur + step
        overlaps = any((cur < a.ends_at and cur_end > a.starts_at) for a in taken)
        if not overlaps:
            slots.append(Slot(start=cur.strftime("%H:%M"), end=cur_end.strftime("%H:%M")))
        cur = cur_end

    return AvailabilityOut(doctor_id=doctor_id, date=fecha, slots=slots)
