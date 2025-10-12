from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, date, time, timedelta
from app.core.deps import get_db, get_current_active_user
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.user import User
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorOut
from app.schemas.availability import AvailabilityOut, Slot

router = APIRouter(prefix="/medicos", tags=["medicos"])

@router.post("", response_model=DoctorOut, status_code=status.HTTP_201_CREATED)
def create_doctor(
    payload: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
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
def list_doctors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return db.query(Doctor).order_by(Doctor.full_name.asc()).all()

@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(404, "Médico no encontrado")
    return doctor

@router.get("/{doctor_id}/disponibilidad", response_model=AvailabilityOut)
def doctor_availability(
    doctor_id: int,
    fecha: str = Query(..., description="YYYY-MM-DD"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
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

@router.put("/{doctor_id}", response_model=DoctorOut)
def update_doctor(
    doctor_id: int,
    payload: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(404, "Médico no encontrado")
    
    # Validar horarios si se están actualizando
    work_start = payload.work_start_hour if payload.work_start_hour is not None else doctor.work_start_hour
    work_end = payload.work_end_hour if payload.work_end_hour is not None else doctor.work_end_hour
    
    if work_end <= work_start:
        raise HTTPException(400, "work_end_hour debe ser mayor a work_start_hour")
    
    # Actualizar solo los campos que no son None
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(doctor, field, value)
    
    db.commit()
    db.refresh(doctor)
    return doctor

@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(404, "Médico no encontrado")
    
    db.delete(doctor)
    db.commit()
    return {"message": "Médico eliminado exitosamente", "id": doctor_id}
