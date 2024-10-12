# from pydantic import BaseModel
# from datetime import datetime
# from typing import List, Optional
# from .gases import Gas
# from .fuels import Fuel

# # FDU schema
# class FDUBase(BaseModel):
#     service_date: Optional[datetime] = None

# class FDUCreate(FDUBase):
#     gases: Gas  
#     fuels: List[Fuel] = []  # Список связанных видов топлива

# class FDU(FDUBase):
#     id: int
#     gases: Gas  
#     fuels: List[Fuel] = []  # Список связанных видов топлива
#     service_date: Optional[datetime] = None

#     class Config:
#         orm_mode = True
#         from_attributes = True