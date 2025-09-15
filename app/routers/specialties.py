from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.specialty import Specialty
from app.schemas.specialty import SpecialtyCreate, SpecialtyOut

router = APIRouter(prefix="/especialidades", tags=["especialidades"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=SpecialtyOut, status_code=status.HTTP_201_CREATED)
def create_specialty(payload: SpecialtyCreate, db: Session = Depends(get_db)):
    exists = db.query(Specialty).filter(Specialty.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=409, detail="La especialidad ya existe")
    obj = Specialty(name=payload.name, description=payload.description)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("", response_model=list[SpecialtyOut])
def list_specialties(db: Session = Depends(get_db)):
    items = db.query(Specialty).order_by(Specialty.name.asc()).all()
    return items
