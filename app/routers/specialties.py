from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_active_user
from app.models.specialty import Specialty
from app.models.user import User
from app.schemas.specialty import SpecialtyCreate, SpecialtyOut

router = APIRouter(prefix="/especialidades", tags=["especialidades"])

@router.post("", response_model=SpecialtyOut, status_code=status.HTTP_201_CREATED)
def create_specialty(
    payload: SpecialtyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    exists = db.query(Specialty).filter(Specialty.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=409, detail="La especialidad ya existe")
    obj = Specialty(name=payload.name, description=payload.description)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("", response_model=list[SpecialtyOut])
def list_specialties(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    items = db.query(Specialty).order_by(Specialty.name.asc()).all()
    return items
