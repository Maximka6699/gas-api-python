# from pydantic import BaseModel
# from datetime import datetime
# from typing import List, Optional


# # Gas schema
# class GasBase(BaseModel):
#     adress: str
#     photo: Optional[str] = None

# class GasCreate(GasBase):
#     from .FDUs import FDU
#     adress: str
#     photo: Optional[str] = None
#     fdus: List[FDU] = []      # Список связанных FDU
#     class Config:
#         orm_mode = True
#         from_attributes = True

# class Gas(GasBase):
#     from .FDUs import FDU
#     from .reviews import Review
#     id: int
#     adress: str
#     photo: Optional[str] = None
#     reviews: List[Review] = []  # Список отзывов для данной заправки
#     fdus: List[FDU] = []      # Список связанных FDU

#     class Config:
#         orm_mode = True
#         from_attributes = True