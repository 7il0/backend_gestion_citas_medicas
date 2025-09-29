from pydantic import BaseModel, Field, EmailStr

class PatientCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    dni: str | None = Field(default=None, max_length=20)

class PatientUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    dni: str | None = Field(default=None, max_length=20)

class PatientOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr | None = None
    phone: str | None = None
    dni: str | None = None

    class Config:
        from_attributes = True
