from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class UserBase(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: Optional[int] = None
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
    id: Optional[int] = None
    service_date: Optional[datetime] = None

class FDUCreate(FDUBase):
    id: Optional[int] = None
    gas_id: int
    # gases: Optional["GasBase"] = None
    fuels: Optional[List[int]] = []  # Список связанных видов топлива

class FDU(FDUBase):
    id: int
    gases: "GasBase"  
    fuels: List["FuelBase"] = []  # Список связанных видов топлива
    service_date: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True

class FDUUpdate(FDU):
    id: Optional[int] = None # не передаем
    gas_id: Optional[int] = None # передаем, чтобы изменить gases
    gases: Optional["GasBase"] = None # не передаем
    fuels: Optional[List[int]] = [] # передаем, чтобы изменить fuels
    service_date: Optional[datetime] = None
# ----------------------------------------------------------------
class FuelBase(BaseModel):
    id: Optional[int] = None
    name: str
    price: float

class FuelCreate(FuelBase):
    name: str
    price: float
    fdus: Optional[List[int]] = []


class Fuel(FuelBase):
    id: int
    fdus: List[FDUBase] = []  # Список связанных FDU
    name: str
    price: float

    class Config:
        orm_mode = True
        from_attributes = True

class FuelUpdate(Fuel):
    id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[float] = None
    fdus: Optional[List[int]] = []
# ----------------------------------------------------------------

class GasBase(BaseModel):
    id: Optional[int] = None
    adress: str
    photo: Optional[str] = None

class GasCreate(GasBase):
    adress: str
    photo: Optional[str] = None
    fdus: Optional[List[int]] = []      # Список связанных FDU
    reviews: Optional[List[int]] = []      # Список связанных отзывов

class Gas(GasBase):
    id: int
    adress: str
    photo: Optional[str] = None
    reviews: List["ReviewBase"] = []  # Список отзывов для данной заправки
    fdus: List[FDUBase] = []      # Список связанных FDU
    class Config:
        orm_mode = True
        from_attributes = True
# ----------------------------------------------------------------

class ReviewBase(BaseModel):
    user_id: Optional[int]
    gas_id: Optional[int]
    text: str
    review_date: Optional[datetime]

class ReviewCreate(ReviewBase):
    text: str
    user_id: Optional[int]
    gas_id: Optional[int]
    review_date: Optional[datetime]

class Review(ReviewBase):
    id: Optional[int]
    user_id: int
    gas_id: int
    text: str
    review_date: datetime
    gas: GasBase

    class Config:
        orm_mode = True
        from_attributes = True

class ReviewUpdate(ReviewBase):
    text: str
    review_date: Optional[datetime]