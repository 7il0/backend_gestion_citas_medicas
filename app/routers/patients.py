from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.db.session import SessionLocal
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientOut

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    if payload.email:
        exists = db.query(Patient).filter(Patient.email == payload.email).first()
        if exists:
            raise HTTPException(409, "El email ya está registrado")
    if payload.dni:
        exists = db.query(Patient).filter(Patient.dni == payload.dni).first()
        if exists:
            raise HTTPException(409, "El DNI ya está registrado")
    obj = Patient(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        dni=payload.dni
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("", response_model=list[PatientOut])
def list_patients(q: str | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Patient)
    if q:
        like = f"%{q.lower()}%"
        query = query.filter(
            or_(
                func.lower(Patient.full_name).like(like),
                func.lower(Patient.email).like(like),
                func.lower(Patient.dni).like(like)
            )
        )
    return query.order_by(Patient.full_name.asc()).all()
