from pydantic import BaseModel, Field

class DoctorCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    specialty_id: int
    work_start_hour: int = Field(ge=0, le=23, default=9)
    work_end_hour: int = Field(ge=0, le=23, default=17)
    slot_minutes: int = Field(ge=5, le=180, default=30)

class DoctorOut(BaseModel):
    id: int
    full_name: str
    specialty_id: int
    work_start_hour: int
    work_end_hour: int
    slot_minutes: int

    class Config:
        from_attributes = True
