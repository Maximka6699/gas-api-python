from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    username: str
    email: str
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    regdate: Optional[date]=None
    loyaltylvl: Optional[str]=1
    score: Optional[int]=50

    class Config:
        orm_mode = True
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str
