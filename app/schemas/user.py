from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=150)

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)

class UserOut(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
