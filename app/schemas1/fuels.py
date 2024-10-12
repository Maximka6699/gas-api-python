# from pydantic import BaseModel
# from datetime import datetime
# from typing import List, Optional


# # Fuel schema
# class FuelCreate(BaseModel):
#     from .FDUs import FDU
#     name: str
#     price: float
#     fdus: List[FDU] = []

# class Fuel(BaseModel):
#     from .FDUs import FDU
#     id: int
#     fdus: List[FDU] = []  # Список связанных FDU
#     name: str
#     price: float

#     class Config:
#         orm_mode = True
#         from_attributes = True