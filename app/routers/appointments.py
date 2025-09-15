from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import timedelta
from app.db.session import SessionLocal
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.schemas.appointment import AppointmentCreate, AppointmentOut

router = APIRouter(prefix="/citas", tags=["citas"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).get(payload.doctor_id)
    if not doctor:
        raise HTTPException(404, "Médico no encontrado")

    start = payload.starts_at
    end = start + timedelta(minutes=payload.duration_minutes)

    # Verifica que esté dentro del horario del médico
    if not (doctor.work_start_hour <= start.hour < doctor.work_end_hour):
        raise HTTPException(400, "Horario fuera de la jornada del médico")

    # Verifica solapamientos
    conflict = db.query(Appointment).filter(
        and_(
            Appointment.doctor_id == payload.doctor_id,
            Appointment.starts_at < end,
            Appointment.ends_at > start
        )
    ).first()
    if conflict:
        raise HTTPException(409, "El horario ya está reservado")

    ap = Appointment(
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        specialty_id=payload.specialty_id,
        appointment_type_id=payload.appointment_type_id,
        starts_at=start,
        ends_at=end,
        status="PROGRAMADA"
    )
    db.add(ap); db.commit(); db.refresh(ap)
    return ap

@router.get("", response_model=list[AppointmentOut])
def list_appointments(
    medicoId: int | None = Query(default=None, alias="medicoId"),
    pacienteId: int | None = Query(default=None, alias="pacienteId"),
    fecha: str | None = Query(default=None, description="YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    q = db.query(Appointment)
    if medicoId:
        q = q.filter(Appointment.doctor_id == medicoId)
    if pacienteId:
        q = q.filter(Appointment.patient_id == pacienteId)
    if fecha:
        try:
            q = q.filter(func.date(Appointment.starts_at) == fecha)
        except Exception:
            raise HTTPException(400, "Fecha inválida, use YYYY-MM-DD")
    return q.order_by(Appointment.starts_at.asc()).all()
