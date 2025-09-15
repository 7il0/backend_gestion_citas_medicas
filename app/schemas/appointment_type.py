from pydantic import BaseModel, Field

class AppointmentTypeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=255)

class AppointmentTypeOut(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
