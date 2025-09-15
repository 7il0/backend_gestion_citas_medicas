from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta
from app.db.session import Base

class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=False)
    specialty_id: Mapped[int] = mapped_column(ForeignKey("specialties.id"), nullable=False)
    appointment_type_id: Mapped[int] = mapped_column(ForeignKey("appointment_types.id"), nullable=False)

    starts_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ends_at:   Mapped[datetime] = mapped_column(DateTime, nullable=False)

    status: Mapped[str] = mapped_column(String(20), default="PROGRAMADA")  # PROGRAMADA/ATENDIDA/CANCELADA

    patient = relationship("Patient")
    doctor = relationship("Doctor")
