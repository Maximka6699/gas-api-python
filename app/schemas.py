from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

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



# ----------------------------------------------------------------
class FDUBase(BaseModel):
    service_date: Optional[datetime] = None

class FDUCreate(FDUBase):
    gases: "Gas"  
    fuels: List["Fuel"] = []  # Список связанных видов топлива

class FDU(FDUBase):
    id: int
    gases: "Gas"  
    fuels: List["Fuel"] = []  # Список связанных видов топлива
    service_date: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True
# ----------------------------------------------------------------

class FuelCreate(BaseModel):
    name: str
    price: float
    fdus: Optional[List[int]] = []


class Fuel(BaseModel):
    id: int
    fdus: List[FDU] = []  # Список связанных FDU
    name: str
    price: float

    class Config:
        orm_mode = True
        from_attributes = True

# ----------------------------------------------------------------

class GasBase(BaseModel):
    adress: str
    photo: Optional[str] = None

class GasCreate(GasBase):
    adress: str
    photo: Optional[str] = None
    fdus: List[FDU] = []      # Список связанных FDU
    class Config:
        orm_mode = True
        from_attributes = True

class Gas(GasBase):
    id: int
    adress: str
    photo: Optional[str] = None
    reviews: List["Review"] = []  # Список отзывов для данной заправки
    fdus: List[FDU] = []      # Список связанных FDU

    class Config:
        orm_mode = True
        from_attributes = True
# ----------------------------------------------------------------

class ReviewCreate(BaseModel):
    text: str
    class Config:
        orm_mode = True
        from_attributes = True


class Review(BaseModel):
    id: int
    user_id: int
    gas_id: int
    text: str
    review_date: datetime

    class Config:
        orm_mode = True
        from_attributes = True