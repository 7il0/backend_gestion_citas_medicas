from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.appointment_type import AppointmentType
from app.schemas.appointment_type import AppointmentTypeCreate, AppointmentTypeOut

router = APIRouter(prefix="/tipos-cita", tags=["tipos-cita"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=AppointmentTypeOut, status_code=status.HTTP_201_CREATED)
def create_appointment_type(payload: AppointmentTypeCreate, db: Session = Depends(get_db)):
    exists = db.query(AppointmentType).filter(AppointmentType.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=409, detail="El tipo de cita ya existe")
    obj = AppointmentType(name=payload.name, description=payload.description)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("", response_model=list[AppointmentTypeOut])
def list_appointment_types(db: Session = Depends(get_db)):
    items = db.query(AppointmentType).order_by(AppointmentType.name.asc()).all()
    return items
