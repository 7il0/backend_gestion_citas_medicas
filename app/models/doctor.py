from sqlalchemy import String, ForeignKey, SmallInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Doctor(Base):
    __tablename__ = "doctors"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)

    specialty_id: Mapped[int] = mapped_column(ForeignKey("specialties.id"), nullable=False)
    specialty = relationship("Specialty")

    work_start_hour: Mapped[int] = mapped_column(SmallInteger, default=9)   # 09:00
    work_end_hour:   Mapped[int] = mapped_column(SmallInteger, default=17)  # 17:00
    slot_minutes:    Mapped[int] = mapped_column(Integer, default=30)       # 30 min por cita
