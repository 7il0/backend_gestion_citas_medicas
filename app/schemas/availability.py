from pydantic import BaseModel
from typing import List

class Slot(BaseModel):
    start: str  # "HH:MM"
    end: str    # "HH:MM"

class AvailabilityOut(BaseModel):
    doctor_id: int
    date: str         # "YYYY-MM-DD"
    slots: List[Slot]
